from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func

from app.database import Base


class InterviewRecord(Base):
    __tablename__ = "interviews"

    id = Integer(primary_key=True, index=True)
    candidate_name = String(255, nullable=True)
    role = String(255, nullable=False)
    resume_summary = Text(nullable=True)
    job_description = Text(nullable=True)
    overall_score = Float(default=0.0)
    feedback = Text(nullable=True)
    created_at = DateTime(timezone=True, server_default=func.now(), default=datetime.utcnow)
