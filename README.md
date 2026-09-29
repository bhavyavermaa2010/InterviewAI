import base64
import re
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import InterviewRecord
from app.services.llm_client import llm_answer_feedback, llm_resume_analysis
from app.services.pdf_parser import extract_pdf_text

app = FastAPI(
    title="InterviewAI API",
    version="0.1.0",
    description="Backend for the InterviewAI platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9\s]+", " ", value.lower()).strip()


def extract_skill_matches(resume_text: str, job_description: str) -> List[str]:
    skill_bank = [
        "python",
        "sql",
        "system design",
        "aws",
        "react",
        "node",
        "javascript",
        "java",
        "docker",
        "kubernetes",
        "microservices",
        "mongodb",
        "postgresql",
        "redis",
        "fastapi",
        "api",
        "communication",
        "leadership",
    ]
    resume_norm = normalize(resume_text)
    jd_norm = normalize(job_description)
    return [skill for skill in skill_bank if skill in resume_norm or skill in jd_norm]


def compute_match_score(resume_text: str, job_description: str) -> int:
    resume_terms = set(normalize(resume_text).split())
    jd_terms = set(normalize(job_description).split())
    common_terms = resume_terms & jd_terms
    score = int((len(common_terms) / max(len(jd_terms), 1)) * 100)
    return max(40, min(98, score))


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


class InterviewEvaluationRequest(BaseModel):
    question: str
    answer: str


class PdfResumeUploadRequest(BaseModel):
    file_name: str
    file_bytes_base64: str


class InterviewCreateRequest(BaseModel):
    candidate_name: Optional[str] = None
    role: str
    resume_summary: Optional[str] = None
    job_description: Optional[str] = None
    overall_score: float = 0.0
    feedback: Optional[str] = None


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok", "service": "InterviewAI API"}


@app.post("/api/resume/analyze")
async def analyze_resume(payload: ResumeAnalysisRequest) -> dict:
    resume_text = payload.resume_text or ""
    job_description = payload.job_description or ""

    heuristic_skills = extract_skill_matches(resume_text, job_description)
    missing_skills = [
        skill for skill in ["system design", "aws", "microservices", "kubernetes", "sql"]
        if skill in normalize(job_description) and skill not in normalize(resume_text)
    ]

    summary = {
        "strengths": ["Problem solving", "Communication", "Project ownership"],
        "areas_to_improve": ["System Design", "DBMS", "Leadership"],
    }

    if "aws" in heuristic_skills:
        summary["strengths"].append("Cloud experience")
    if "sql" in heuristic_skills:
        summary["strengths"].append("Data handling")

    llm_result: Dict[str, Any] = {}
    try:
        llm_result = await llm_resume_analysis(resume_text, job_description)
    except Exception:
        llm_result = {}

    if llm_result:
        if llm_result.get("strengths"):
            summary["strengths"] = llm_result["strengths"]
        if llm_result.get("areas_to_improve"):
            summary["areas_to_improve"] = llm_result["areas_to_improve"]
        if llm_result.get("missing_skills"):
            missing_skills = llm_result["missing_skills"]
        if llm_result.get("skills_found"):
            heuristic_skills = llm_result["skills_found"]

    return {
        "candidate_summary": summary,
        "extracted_skills": heuristic_skills,
        "missing_skills": missing_skills,
        "match_score": llm_result.get("match_score") or compute_match_score(resume_text, job_description),
    }


@app.post("/api/resume/upload-pdf")
def upload_pdf(payload: PdfResumeUploadRequest) -> dict:
    try:
        file_bytes = base64.b64decode(payload.file_bytes_base64)
        text = extract_pdf_text(file_bytes)
        return {
            "file_name": payload.file_name,
            "extracted_text": text[:4000],
            "status": "ok",
        }
    except Exception as exc:
        return {"file_name": payload.file_name, "error": str(exc), "status": "failed"}


@app.post("/api/mock-interview/start")
def start_mock_interview() -> dict:
    return {
        "interview_id": "int_101",
        "questions": [
            "Tell me about a project you led and the impact it had.",
            "How do you design a scalable backend for a product with growing traffic?",
            "Walk me through how you would optimize a slow SQL query.",
            "Describe a time when you handled ambiguity in a technical project.",
        ],
    }


@app.post("/api/mock-interview/evaluate")
async def evaluate_answer(payload: InterviewEvaluationRequest) -> dict:
    answer_norm = normalize(payload.answer)

    technical_accuracy = 74
    communication = 80
    problem_solving = 76

    if any(keyword in answer_norm for keyword in ["system design", "architecture", "scalability", "database", "latency", "tradeoff"]):
        technical_accuracy += 12
        problem_solving += 8
    if any(keyword in answer_norm for keyword in ["because", "therefore", "first", "then", "finally", "example", "impact"]):
        communication += 10
    if any(keyword in answer_norm for keyword in ["bottleneck", "monitor", "optimize", "fallback", "error handling", "metrics"]):
        problem_solving += 10

    overall_score = min(98, max(55, round((technical_accuracy + communication + problem_solving) / 3)))

    feedback = "Strong answer with clear structure. Add more depth in trade-offs, failure modes, and impact metrics."
    improvement_tip = "Include a concise problem statement, architecture trade-offs, and a verification or optimization strategy."

    try:
        llm_feedback = await llm_answer_feedback(payload.question, payload.answer)
        if llm_feedback:
            if llm_feedback.get("feedback"):
                feedback = llm_feedback["feedback"]
            if llm_feedback.get("improvement_tip"):
                improvement_tip = llm_feedback["improvement_tip"]
    except Exception:
        pass

    return {
        "overall_score": overall_score,
        "technical_accuracy": min(98, technical_accuracy),
        "communication": min(98, communication),
        "problem_solving": min(98, problem_solving),
        "feedback": feedback,
        "improvement_tip": improvement_tip,
    }


@app.post("/api/interviews")
def create_interview(payload: InterviewCreateRequest, db: Session = Depends(get_db)) -> dict:
    interview = InterviewRecord(
        candidate_name=payload.candidate_name,
        role=payload.role,
        resume_summary=payload.resume_summary,
        job_description=payload.job_description,
        overall_score=payload.overall_score,
        feedback=payload.feedback,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return {
        "id": interview.id,
        "candidate_name": interview.candidate_name,
        "role": interview.role,
        "overall_score": interview.overall_score,
        "feedback": interview.feedback,
    }


@app.get("/api/interviews")
def list_interviews(db: Session = Depends(get_db)) -> list[dict]:
    interviews = db.query(InterviewRecord).order_by(InterviewRecord.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "candidate_name": item.candidate_name,
            "role": item.role,
            "overall_score": item.overall_score,
            "feedback": item.feedback,
            "created_at": item.created_at.isoformat() if item.created_at else None,
        }
        for item in interviews
    ]


@app.get("/api/interviews/{interview_id}")
def get_interview(interview_id: int, db: Session = Depends(get_db)) -> dict:
    interview = db.query(InterviewRecord).filter(InterviewRecord.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return {
        "id": interview.id,
        "candidate_name": interview.candidate_name,
        "role": interview.role,
        "resume_summary": interview.resume_summary,
        "job_description": interview.job_description,
        "overall_score": interview.overall_score,
        "feedback": interview.feedback,
        "created_at": interview.created_at.isoformat() if interview.created_at else None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
