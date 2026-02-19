from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Run
from app.extensions import db

bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@bp.get("/")
@login_required
def dashboard():
    q = Run.query.filter_by(user_id=current_user.id)

    total_runs = q.count()
    avg_before = q.with_entities(func.avg(Run.match_score_before)).scalar() or 0
    avg_after = q.with_entities(func.avg(Run.match_score_after)).scalar() or 0
    improved = q.filter(Run.match_score_after > Run.match_score_before).count()

    last10 = q.order_by(Run.created_at.desc()).limit(10).all()

    return render_template(
        "analytics.html",
        total_runs=total_runs,
        avg_before=round(float(avg_before), 2),
        avg_after=round(float(avg_after), 2),
        improved=improved,
        last10=last10,
    )
