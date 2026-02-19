import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Run

from app.agents.extractor import extract_maps
from app.agents.recruiter import recruiter_match
from app.agents.optimizer import optimize_cv
from app.agents.ats import ats_audit, ats_submission_cv
from app.agents.interview import interview_pack

bp = Blueprint("flow", __name__)

def _safe_json_loads(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None

@bp.get("/")
@login_required
def index():
    runs = Run.query.filter_by(user_id=current_user.id).order_by(Run.created_at.desc()).limit(20).all()
    return render_template("index.html", runs=runs)

@bp.get("/run")
@login_required
def run_form():
    return render_template("run.html")

@bp.post("/run")
@login_required
def run_submit():
    cv = request.form["cv"].strip()
    job_ad = request.form["job_ad"].strip()
    cover = (request.form.get("cover_letter") or "").strip() or None
    target_role = (request.form.get("target_role") or "").strip() or None

    if not cv or not job_ad:
        flash("CV and Job Ad are required.")
        return redirect(url_for("flow.run_form"))

    r = Run(
        user_id=current_user.id,
        cv_text=cv,
        job_ad_text=job_ad,
        cover_letter_text=cover,
        target_role=target_role,
    )
    db.session.add(r)
    db.session.commit()

    # 0) Extract structured maps (stored in match_before_json for MVP)
    extracted = extract_maps(cv, job_ad)

    # 1) Recruiter match (before)
    match_before = recruiter_match(cv, job_ad, target_role)
    r.match_before_json = json.dumps({
        "extracted": extracted,
        "match": match_before
    })

    mb = _safe_json_loads(match_before)
    if mb and "match_score" in mb:
        try:
            r.match_score_before = float(mb["match_score"])
        except Exception:
            r.match_score_before = None

    # 2) Optimize CV (Professional Experience rewrite)
    optimized_section = optimize_cv(cv, match_before, target_role)
    r.optimized_cv = optimized_section

    # 3) ATS audit + ATS submission CV
    ats_risks = ats_audit(optimized_section)
    r.ats_risks_json = ats_risks
    r.ats_ready_cv = ats_submission_cv(optimized_section)

    # 4) Re-score after optimization (iteration loop)
    match_after = recruiter_match(r.ats_ready_cv or optimized_section, job_ad, target_role)
    r.match_after_json = match_after

    ma = _safe_json_loads(match_after)
    if ma and "match_score" in ma:
        try:
            r.match_score_after = float(ma["match_score"])
        except Exception:
            r.match_score_after = None

    # 5) Interview pack
    r.interview_pack = interview_pack(r.ats_ready_cv or optimized_section, job_ad, target_role)

    db.session.commit()
    return redirect(url_for("flow.result", run_id=r.id))

@bp.get("/result/<int:run_id>")
@login_required
def result(run_id: int):
    r = Run.query.filter_by(id=run_id, user_id=current_user.id).first_or_404()

    # Pretty print some JSON fields if valid
    match_before = None
    match_after = None
    ats_risks = None

    try:
        stored = json.loads(r.match_before_json) if r.match_before_json else None
        match_before = json.loads(stored["match"]) if stored and "match" in stored else None
    except Exception:
        match_before = None

    try:
        match_after = json.loads(r.match_after_json) if r.match_after_json else None
    except Exception:
        match_after = None

    try:
        ats_risks = json.loads(r.ats_risks_json) if r.ats_risks_json else None
    except Exception:
        ats_risks = None

    return render_template(
        "result.html",
        run=r,
        match_before=match_before,
        match_after=match_after,
        ats_risks=ats_risks
    )
