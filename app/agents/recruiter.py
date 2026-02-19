from app.services.openai_client import llm_text

def recruiter_match(cv: str, job_ad: str, target_role: str | None) -> str:
    system = "You are a senior recruiter. Be brutally honest. No fluff."
    user = f"""
Role: {target_role or "N/A"}

Compare CV vs Job Ad. Return JSON ONLY:
{{
  "match_score": 0-100,
  "short_reason": "...",
  "top_5_gaps": ["...", "..."],
  "hireability_blockers": ["..."]
}}

CV:
{cv}

JOB AD:
{job_ad}
"""
    return llm_text(system, user)
