# AI Job Hunting System (Flask) — Full Version

This is a production-ready Flask web app that:
- Accepts CV + Job Ad (+ optional cover letter & target role)
- Runs a multi-agent LLM pipeline:
  - Recruiter match (score + gaps)
  - CV optimizer (Google X-Y-Z bullets, no invented metrics)
  - ATS audit (parsing risks) + ATS submission CV ("ugly but deadly")
  - Re-score after optimization (delta)
  - Interview pack (technical, HR/values, candidate questions)
- Stores results in DB (SQLite locally; Postgres on Railway)
- Includes login/registration + analytics dashboard

## Local Run (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env with OPENAI_API_KEY and SECRET_KEY

export FLASK_APP=app       # Windows: set FLASK_APP=app
flask run
```

Open: http://127.0.0.1:5000

## Production-like local run (Gunicorn)

```bash
gunicorn "app:create_app()" --bind 0.0.0.0:8000 --workers 2 --threads 4 --timeout 180
```

## Railway Deploy

1) Push this repo to GitHub  
2) Railway → New Project → Deploy from GitHub  
3) Add Postgres plugin (Railway sets `DATABASE_URL`)  
4) Set env vars in Railway:
- `OPENAI_API_KEY`
- `SECRET_KEY`
- optionally `OPENAI_MODEL`

Done ✅

## Security note
This MVP stores raw CV/job text in the database for convenience. For production, consider:
- Redaction/encryption of PII
- Short retention policy
- User delete/export controls
