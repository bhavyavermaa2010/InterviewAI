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
    response = await generate_text(prompt)
    if not response:
        return {}

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}
