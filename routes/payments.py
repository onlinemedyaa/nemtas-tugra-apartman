from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Payment, Due, Flat

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

@payments_bp.route("/add", methods=["POST"])
@login_required
def add_payment():
    amount = float(request.form.get("amount") or 0)
    flat_id = int(request.form.get("flat_id"))
    month = request.form.get("month")

    payment = Payment(user_id=current_user.id, amount=amount)
    db.session.add(payment)

    due = Due.query.filter_by(flat_id=flat_id, month=month).first()
    if not due:
        flash("Bu daire/ay için aidat bulunamadı. Önce aidat hesaplayın.", "danger")
        return redirect(url_for("dashboard.admin_dashboard"))

    due.paid_amount += amount
    due.balance = due.per_flat_due - due.paid_amount

    db.session.commit()
    flash("Ödeme eklendi.", "success")
    return redirect(url_for("dashboard.admin_dashboard"))
