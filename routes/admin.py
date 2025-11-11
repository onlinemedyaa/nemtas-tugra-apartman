from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Flat, AuditLog

admin_bp = Blueprint('admin', __name__)

def require_admin():
    return current_user.is_authenticated and current_user.role == "admin"

@admin_bp.route("/admin/users", methods=["GET", "POST"])
@login_required
def users_admin():
    if not require_admin():
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get("name")
        role = request.form.get("role", "resident")
        pin = request.form.get("pin", "123456")
        user = User(phone=phone, name=name, role=role, pin_hash=generate_password_hash(pin))
        db.session.add(user)
        db.session.commit()
        db.session.add(AuditLog(user_id=current_user.id, action="create", entity="user", entity_id=user.id,
                                details=f"{name} ({phone}) rol={role}"))
        db.session.commit()
        flash("Kullanıcı eklendi.", "success")
    users = User.query.order_by(User.id.desc()).all()
    flats = Flat.query.order_by(Flat.code.asc()).all()
    return render_template("users_admin.html", users=users, flats=flats)

@admin_bp.route("/admin/assign", methods=["POST"])
@login_required
def assign_flat():
    if not require_admin():
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("dashboard"))
    user_id = int(request.form.get("user_id"))
    flat_id = int(request.form.get("flat_id"))
    flat = Flat.query.get(flat_id)
    flat.resident_user_id = user_id
    db.session.commit()
    db.session.add(AuditLog(user_id=current_user.id, action="update", entity="flat", entity_id=flat_id,
                            details=f"Flat {flat.code} -> user {user_id}"))
    db.session.commit()
    flash("Daire atandı.", "success")
    return redirect(url_for("admin.users_admin"))
