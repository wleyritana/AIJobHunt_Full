from app.services.openai_client import llm_text

def interview_pack(cv: str, job_ad: str, target_role: str | None) -> str:
    system = "You are a hiring manager + HR partner. Be concrete and role-specific."
    user = f"""
Role: {target_role or "N/A"}

Generate an interview pack with clear headings:

A) Technical (3):
- Question
- Perfect answer based on CV (no invented experience)
- What it tests

B) HR/Values (3):
- Question
- What HR assesses
- Strong answer tailored to CV

C) Candidate questions (3):
- Question to ask
- Why it matters
- Green flags
- Red flags

CV:
{cv}

JOB AD:
{job_ad}
"""
    return llm_text(system, user)
