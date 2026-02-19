from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    runs = db.relationship("Run", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    target_role = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cv_text = db.Column(db.Text, nullable=False)
    job_ad_text = db.Column(db.Text, nullable=False)
    cover_letter_text = db.Column(db.Text, nullable=True)

    # Outputs
    match_score_before = db.Column(db.Float, nullable=True)
    match_score_after = db.Column(db.Float, nullable=True)

    # Stored as JSON-ish strings for MVP
    match_before_json = db.Column(db.Text, nullable=True)  # includes gaps
    match_after_json = db.Column(db.Text, nullable=True)

    optimized_cv = db.Column(db.Text, nullable=True)
    ats_risks_json = db.Column(db.Text, nullable=True)
    ats_ready_cv = db.Column(db.Text, nullable=True)

    interview_pack = db.Column(db.Text, nullable=True)

class JobAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
