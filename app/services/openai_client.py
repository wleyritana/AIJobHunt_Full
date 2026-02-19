from openai import OpenAI
from flask import current_app

def _client() -> OpenAI:
    return OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

def llm_text(system: str, user: str) -> str:
    model = current_app.config["OPENAI_MODEL"]
    client = _client()
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return resp.output_text
