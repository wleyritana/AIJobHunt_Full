from app.services.openai_client import llm_text

def extract_maps(cv: str, job_ad: str) -> str:
    system = "You extract structured information. Output strict JSON only."
    user = f"""
Return JSON with keys:
- job_map: {{ must_have:[], nice_to_have:[], tools:[], seniority_signals:[], responsibilities:[] }}
- candidate_map: {{ skills:[], tools:[], roles:[], achievements:[], leadership_signals:[], domains:[] }}
- taxonomy: {{ synonyms:{{}} }}

CV:
{cv}

JOB AD:
{job_ad}
"""
    return llm_text(system, user)
