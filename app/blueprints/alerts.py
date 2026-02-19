from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import JobAlert

bp = Blueprint("alerts", __name__, url_prefix="/alerts")

@bp.get("/")
@login_required
def alerts():
    alerts = JobAlert.query.filter_by(user_id=current_user.id).order_by(JobAlert.created_at.desc()).all()
    return render_template("alerts.html", alerts=alerts)

@bp.post("/create")
@login_required
def create_alert():
    keyword = (request.form.get("keyword") or "").strip()
    location = (request.form.get("location") or "").strip() or None
    if not keyword:
        flash("Keyword is required.")
        return redirect(url_for("alerts.alerts"))

    a = JobAlert(user_id=current_user.id, keyword=keyword, location=location, is_enabled=True)
    db.session.add(a)
    db.session.commit()
    flash("Alert created (stub).")
    return redirect(url_for("alerts.alerts"))

@bp.post("/toggle/<int:alert_id>")
@login_required
def toggle(alert_id: int):
    a = JobAlert.query.filter_by(id=alert_id, user_id=current_user.id).first_or_404()
    a.is_enabled = not a.is_enabled
    db.session.commit()
    return redirect(url_for("alerts.alerts"))
