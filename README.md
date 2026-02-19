# AI Job Hunting System (Lite Secure Console)

Public Flask web app (no database) with:
- Shared access password gate (session cookie)
- IP rate limit (3 runs/hour)
- Global daily cap (default 20/day, per instance)
- Developer-console UI with syntax-highlighted JSON (Prism.js CDN)
- Railway-ready Procfile

## Local run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# set OPENAI_API_KEY, SECRET_KEY, ACCESS_PASSWORD

flask --app app run
```
Open http://127.0.0.1:5000

## Railway
1) Push to GitHub
2) Railway → New Project → Deploy from GitHub
3) Set env vars:
- OPENAI_API_KEY
- OPENAI_MODEL (optional)
- SECRET_KEY
- ACCESS_PASSWORD
- DAILY_CAP=20
