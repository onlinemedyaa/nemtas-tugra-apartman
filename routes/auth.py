from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/")

# Giriş sayfası
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        pin = request.form.get("pin")

        user = User.query.filter_by(phone=phone).first()
        if user and check_password_hash(user.pin_hash, pin):
            login_user(user)
            flash("Giriş başarılı", "success")
            if user.role == "admin":
                return redirect(url_for("dashboard.admin_dashboard"))
            else:
                return redirect(url_for("dashboard.resident_dashboard"))
        else:
            flash("Telefon veya PIN hatalı", "danger")

    return render_template("login.html")

# Çıkış
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Çıkış yapıldı", "info")
    return redirect(url_for("auth.login"))
