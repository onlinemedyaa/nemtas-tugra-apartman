from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        pin = request.form.get("pin", "").strip()

        user = User.query.filter_by(phone=phone).first()

        if user and check_password_hash(user.pin_hash, pin):
            login_user(user)
            flash("Giriş başarılı.", "success")

            # Kullanıcı rolüne göre yönlendirme
            if user.role == "admin":
                return redirect(url_for("dashboard.admin_dashboard"))
            elif user.role == "resident":
                return redirect(url_for("dashboard.resident_dashboard"))
            else:
                flash("Tanımsız kullanıcı rolü.", "danger")
                return redirect(url_for("auth.login"))
        else:
            flash("Telefon veya PIN hatalı.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("auth.login"))
