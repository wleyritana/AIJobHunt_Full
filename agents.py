from openai_client import llm_text

def recruiter_match(cv: str, job_ad: str, role: str | None) -> str:
    system = "You are a senior recruiter. Be brutally honest and specific. No fluff."
    user = f"""
Role: {role or "N/A"}

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

def optimize_experience(cv: str, match_json: str, role: str | None) -> str:
    system = "You are a senior CV consultant. Use Google X-Y-Z. Never invent metrics."
    user = f"""
Role: {role or "N/A"}

Recruiter match JSON:
{match_json}

Rewrite ONLY the Professional Experience section (or equivalent).
- Integrate missing keywords naturally
- Use X-Y-Z bullets where possible
- If metrics missing, use [metric needed]

Return plain text only.

CV:
{cv}
"""
    return llm_text(system, user)

def ats_audit(cv_text: str) -> str:
    system = "You are an ATS (Workday/SuccessFactors). Focus on parsing risks and fixes."
    user = f"""
Return JSON ONLY:
{{
  "risks": [
    {{"issue":"...", "risk":"low|medium|high", "fix":"..."}}
  ]
}}

CV:
{cv_text}
"""
    return llm_text(system, user)

def ats_submission_cv(cv_text: str) -> str:
    system = "You generate ATS-maximized CVs. One column. Standard headings. No tables/icons."
    user = f"""
Create an ATS submission CV:
- One column
- Standard headings: Summary, Skills, Work Experience, Education, Certifications (if any)
- High keyword density without stuffing
- Functional over aesthetic (“ugly but deadly”)

Return plain text only.

CV:
{cv_text}
"""
    return llm_text(system, user)

def interview_pack(cv_text: str, job_ad: str, role: str | None) -> str:
    system = "You are a hiring manager + HR partner. Be concrete and role-specific."
    user = f"""
Role: {role or "N/A"}

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
- Question
- Why it matters
- Green flags
- Red flags

Return plain text only.

CV:
{cv_text}

JOB AD:
{job_ad}
"""
    return llm_text(system, user)
