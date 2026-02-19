from app.services.openai_client import llm_text

def culture_analysis(company_material: str, reviews: str) -> str:
    system = "You are a neutral culture analyst. Summarize themes; compare branding vs reviews."
    user = f"""
Compare:
1) Employer branding / company culture material
2) Employee reviews (Glassdoor/Indeed-like)

Return:
- Alignments
- Differences
- Contradictions
- Practical implications for candidate

Company material:
{company_material}

Reviews:
{reviews}
"""
    return llm_text(system, user)
