from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Due, Flat
from services.dues import generate_dues

dues_bp = Blueprint('dues', __name__)

@dues_bp.route("/admin/dues/generate", methods=["POST"])
@login_required
def generate():
    if current_user.role != "admin":
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("dashboard"))
    month = request.form.get("month")
    result = generate_dues(month)
    flash(f"{month} için aidatlar hesaplandı.", "success")
    return redirect(url_for("dues.list_dues", month=month))

@dues_bp.route("/dues", methods=["GET"])
@login_required
def list_dues():
    month = request.args.get("month")
    q = Due.query
    if current_user.role == "resident":
        flat = Flat.query.filter(Flat.resident_user_id == current_user.id).first()
        if flat:
            q = q.filter(Due.flat_id == flat.id)
    if month:
        q = q.filter(Due.month == month)
    items = q.order_by(Due.flat_id.asc()).all()
    return render_template("dues.html", items=items, month=month)
