from app.services.openai_client import llm_text

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
- Standard headings: Summary, Skills, Work Experience, Education, Certifications (if present)
- High keyword density without stuffing
- Functional over aesthetic (“ugly but deadly”)

Return plain text only.

CV:
{cv_text}
"""
    return llm_text(system, user)
