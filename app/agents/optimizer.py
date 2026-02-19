from app.services.openai_client import llm_text

def optimize_cv(cv: str, match_json: str, target_role: str | None) -> str:
    system = "You are a senior CV consultant. Use Google X-Y-Z. Never invent metrics."
    user = f"""
Role: {target_role or "N/A"}

Recruiter match JSON (contains gaps):
{match_json}

Task:
Rewrite ONLY the Professional Experience section (or equivalent).
- Integrate missing keywords naturally.
- Use X-Y-Z bullets where possible:
  Achieved X, measured by Y, by doing Z.
- If metrics are missing, use placeholders like: [metric needed]
Return plain text only.

CV:
{cv}
"""
    return llm_text(system, user)
