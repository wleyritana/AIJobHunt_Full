from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/register")
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for("flow.index"))
    return render_template("register.html")

@bp.post("/register")
def register():
    email = request.form["email"].strip().lower()
    password = request.form["password"]

    if User.query.filter_by(email=email).first():
        flash("Email already registered.")
        return redirect(url_for("auth.register_form"))

    u = User(email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    login_user(u)
    return redirect(url_for("flow.index"))

@bp.get("/login")
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for("flow.index"))
    return render_template("login.html")

@bp.post("/login")
def login():
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    u = User.query.filter_by(email=email).first()

    if not u or not u.check_password(password):
        flash("Invalid credentials.")
        return redirect(url_for("auth.login_form"))

    login_user(u)
    return redirect(url_for("flow.index"))

@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_form"))
