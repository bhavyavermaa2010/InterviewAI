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


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok", "service": "InterviewAI API"}


@app.post("/api/resume/analyze")
def analyze_resume(payload: ResumeAnalysisRequest) -> dict:
    resume = payload.resume_text.lower()
    jd = payload.job_description.lower()

    extracted_skills = [
        skill for skill in ["python", "sql", "system design", "aws", "react", "node.js", "java", "docker"]
        if skill in resume or skill in jd
    ]

    missing_skills = [
        skill for skill in ["system design", "aws", "kafka", "microservices"]
        if skill in jd and skill not in resume
    ]

    return {
        "candidate_summary": {
            "strengths": ["Problem solving", "Communication", "Project ownership"],
            "areas_to_improve": ["System Design", "DBMS", "Leadership"]
        },
        "extracted_skills": extracted_skills,
        "missing_skills": missing_skills,
        "match_score": 82,
    }


@app.post("/api/mock-interview/start")
def start_mock_interview() -> dict:
    return {
        "interview_id": "int_101",
        "questions": [
            "Tell me about a project you led and the impact it had.",
            "How do you design a scalable backend for a product with growing traffic?",
            "Walk me through how you would optimize a slow SQL query."
        ]
    }


@app.post("/api/mock-interview/evaluate")
def evaluate_answer() -> dict:
    return {
        "overall_score": 84,
        "technical_accuracy": 86,
        "communication": 82,
        "problem_solving": 80,
        "feedback": "Strong answer with good structure. Add more depth in system design trade-offs and performance considerations.",
        "improvement_tip": "Discuss bottlenecks, scaling strategies, and fallback plans more explicitly."
    }
