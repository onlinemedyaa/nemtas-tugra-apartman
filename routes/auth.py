from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from models import db, User
from services.auth import verify_pin, validate_phone
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

class LoginUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.role = user.role

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        pin = request.form.get("pin", "").strip()
        if not validate_phone(phone):
            flash("Geçersiz telefon.", "danger")
            return render_template("login.html")
        user = User.query.filter_by(phone=phone).first()
        if not user or not verify_pin(user.pin_hash, pin):
            flash("Telefon veya PIN hatalı.", "danger")
            return render_template("login.html")
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/set-pin", methods=["GET", "POST"])
@login_required
def set_pin():
    if request.method == "POST":
        new_pin = request.form.get("pin", "").strip()
        if len(new_pin) != 6 or not new_pin.isdigit():
            flash("PIN 6 haneli olmalı.", "danger")
            return render_template("profile.html")
        user = User.query.get(current_user.id)
        user.pin_hash = generate_password_hash(new_pin)
        db.session.commit()
        flash("PIN güncellendi.", "success")
    return render_template("profile.html")
