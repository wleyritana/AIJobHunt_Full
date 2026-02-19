import os
import json
from datetime import date
from threading import Lock

from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from agents import recruiter_match, optimize_experience, ats_audit, ats_submission_cv, interview_pack

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

# Rate limiting (per IP)
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

# Global daily cap (per instance)
DAILY_CAP = int(os.getenv("DAILY_CAP", "20"))
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD", "")
_usage = {"day": str(date.today()), "count": 0}
_lock = Lock()

def _reset_if_new_day():
    global _usage
    today = str(date.today())
    if _usage["day"] != today:
        _usage = {"day": today, "count": 0}

def remaining_today() -> int:
    with _lock:
        _reset_if_new_day()
        return max(0, DAILY_CAP - _usage["count"])

def check_and_increment_cap() -> bool:
    global _usage
    today = str(date.today())
    with _lock:
        if _usage["day"] != today:
            _usage = {"day": today, "count": 0}
        if _usage["count"] >= DAILY_CAP:
            return False
        _usage["count"] += 1
        return True

def pretty_json(text: str) -> str:
    try:
        return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except Exception:
        return text

@app.get("/")
def home():
    return render_template(
        "index.html",
        unlocked=bool(session.get("authed")),
        remaining=remaining_today(),
        daily_cap=DAILY_CAP,
    )

@app.post("/unlock")
@limiter.limit("10/minute")
def unlock():
    key = (request.form.get("access_key") or "").strip()
    if not ACCESS_PASSWORD:
        return render_template("index.html", error="Server misconfigured: ACCESS_PASSWORD not set.", unlocked=False, remaining=remaining_today(), daily_cap=DAILY_CAP)

    if key == ACCESS_PASSWORD:
        session["authed"] = True
        return redirect(url_for("home"))

    return render_template("index.html", error="Invalid access key.", unlocked=False, remaining=remaining_today(), daily_cap=DAILY_CAP)

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.post("/run")
@limiter.limit("3/hour")
def run():
    if not session.get("authed"):
        return render_template("index.html", error="Access key required.", unlocked=False, remaining=remaining_today(), daily_cap=DAILY_CAP)

    if not check_and_increment_cap():
        return render_template("index.html", error=f"Daily capacity reached ({DAILY_CAP}/day). Try again tomorrow.", unlocked=True, remaining=remaining_today(), daily_cap=DAILY_CAP)

    role = (request.form.get("target_role") or "").strip() or None
    cv = (request.form.get("cv") or "").strip()
    job_ad = (request.form.get("job_ad") or "").strip()

    if not cv or not job_ad:
        return render_template("index.html", error="CV and Job Ad are required.", unlocked=True, remaining=remaining_today(), daily_cap=DAILY_CAP)

    # Input length limits
    if len(cv) > 8000 or len(job_ad) > 8000:
        return render_template("index.html", error="Inputs too long. Keep CV and Job Ad under 8000 characters each.", unlocked=True, remaining=remaining_today(), daily_cap=DAILY_CAP)

    # Pipeline
    match_before = recruiter_match(cv, job_ad, role)
    optimized = optimize_experience(cv, match_before, role)
    risks = ats_audit(optimized)
    ats_cv = ats_submission_cv(optimized)
    match_after = recruiter_match(ats_cv, job_ad, role)
    interview = interview_pack(ats_cv, job_ad, role)

    return render_template(
        "result.html",
        role=role,
        match_before_pretty=pretty_json(match_before),
        risks_pretty=pretty_json(risks),
        match_after_pretty=pretty_json(match_after),
        optimized=optimized,
        ats_cv=ats_cv,
        interview=interview,
        remaining=remaining_today(),
        daily_cap=DAILY_CAP,
    )

@app.get("/health")
def health():
    return {"status": "ok"}
