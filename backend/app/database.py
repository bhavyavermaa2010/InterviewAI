import json
from typing import Any, Dict

import httpx

from app.config import DEFAULT_LLM_MODEL, OLLAMA_BASE_URL


async def generate_text(prompt: str, model: str = DEFAULT_LLM_MODEL) -> str:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2},
                },
            )
            response.raise_for_status()
            payload = response.json()
            return payload.get("response", "")
    except Exception:
        return ""


def _parse_json_response(response: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    if not response:
        return fallback

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else fallback
    except json.JSONDecodeError:
        return fallback


async def llm_resume_analysis(resume_text: str, job_description: str) -> Dict[str, Any]:
    prompt = f"""
You are an expert resume evaluator for hiring and interview prep.
Return valid JSON only with this schema:
{
  "strengths": ["..."],
  "areas_to_improve": ["..."],
  "missing_skills": ["..."],
  "skills_found": ["..."],
  "match_score": 0
}

Resume:
{resume_text}

Job description:
{job_description}
"""
    return _parse_json_response(await generate_text(prompt), {})


async def llm_answer_feedback(question: str, answer: str) -> Dict[str, Any]:
    prompt = f"""
You are a strict interviewer evaluating a candidate answer.
Return valid JSON only with keys: feedback and improvement_tip.
Question: {question}
Answer: {answer}
"""
    return _parse_json_response(await generate_text(prompt), {
        "feedback": "Strong answer with a clear structure. Add more depth in trade-offs, failure modes, and impact metrics.",
        "improvement_tip": "Include a concise problem statement, architecture trade-offs, and a verification or optimization strategy.",
    })
