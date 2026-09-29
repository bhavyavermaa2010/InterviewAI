import re
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9\s]+", " ", value.lower()).strip()


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


class InterviewEvaluationRequest(BaseModel):
    question: str
    answer: str


class InterviewStartRequest(BaseModel):
    role: Optional[str] = None
    resume_summary: Optional[str] = None


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok", "service": "InterviewAI API"}


@app.post("/api/resume/analyze")
def analyze_resume(payload: ResumeAnalysisRequest) -> dict:
    resume_norm = normalize(payload.resume_text)
    jd_norm = normalize(payload.job_description)

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

    extracted_skills = []
    for skill in skill_bank:
        if skill in resume_norm or skill in jd_norm:
            extracted_skills.append(skill)

    jd_terms = set(jd_norm.split())
    resume_terms = set(resume_norm.split())
    common_terms = jd_terms.intersection(resume_terms)
    match_score = min(98, max(40, round((len(common_terms) / max(len(jd_terms), 1)) * 100)))

    missing_skills = [skill for skill in ["system design", "aws", "microservices", "kubernetes", "sql"] if skill in jd_norm and skill not in resume_norm]

    candidate_summary = {
        "strengths": ["Problem solving", "Communication", "Project ownership"],
        "areas_to_improve": ["System Design", "DBMS", "Leadership"],
    }

    if "aws" in extracted_skills and "sql" in extracted_skills:
        candidate_summary["strengths"].append("Cloud and data handling")

    if "leadership" in jd_norm and "leadership" not in resume_norm:
        candidate_summary["areas_to_improve"].append("Leadership communication")

    return {
        "candidate_summary": candidate_summary,
        "extracted_skills": extracted_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
    }


@app.post("/api/mock-interview/start")
def start_mock_interview(payload: Optional[InterviewStartRequest] = None) -> dict:
    questions = [
        "Tell me about a project you led and the impact it had.",
        "How do you design a scalable backend for a product with growing traffic?",
        "Walk me through how you would optimize a slow SQL query.",
        "Describe a time when you handled ambiguity in a technical project.",
    ]

    if payload and payload.role:
        role = payload.role.lower()
        if "backend" in role:
            questions = [
                "Design a scalable backend architecture for a real-time product feed.",
                "How would you improve the reliability of a service under heavy load?",
                "Explain the trade-offs between SQL and NoSQL for a growing product.",
            ]

    return {
        "interview_id": "int_101",
        "questions": questions,
    }


@app.post("/api/mock-interview/evaluate")
def evaluate_answer(payload: InterviewEvaluationRequest) -> dict:
    answer_norm = normalize(payload.answer)
    question_norm = normalize(payload.question)

    score = 72
    technical_accuracy = 75
    communication = 78
    problem_solving = 76

    if any(keyword in answer_norm for keyword in ["system design", "architecture", "scalability", "tradeoff", "latency", "database"]):
        technical_accuracy += 12
        problem_solving += 8

    if any(keyword in answer_norm for keyword in ["first", "then", "because", "therefore", "finally", "example", "impact"]):
        communication += 10

    if any(keyword in answer_norm for keyword in ["monitor", "metrics", "bottleneck", "optimize", "fallback", "error handling"]):
        problem_solving += 10

    overall_score = min(98, max(55, round((technical_accuracy + communication + problem_solving) / 3)))

    feedback = "Strong answer with a clear structure. Add more specific trade-offs and measurable impact to make the response stronger."
    if "scalability" not in answer_norm and "architecture" not in answer_norm:
        feedback = "Good foundation, but the answer would be stronger with more architecture and scaling details."

    improvement_tip = "Include a clear problem statement, the trade-offs you considered, and how you validated the solution using metrics or constraints."

    return {
        "overall_score": overall_score,
        "technical_accuracy": min(98, technical_accuracy),
        "communication": min(98, communication),
        "problem_solving": min(98, problem_solving),
        "feedback": feedback,
        "improvement_tip": improvement_tip,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

