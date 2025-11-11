from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Due, Flat, Expense

dues_bp = Blueprint("dues", __name__, url_prefix="/dues")

@dues_bp.route("/calculate", methods=["POST", "GET"])
@login_required
def calculate_dues():
    if current_user.role != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("dashboard.resident_dashboard"))

    if request.method == "POST":
        month = request.form.get("month")
        scope = request.form.get("scope") or "all"

        flats = Flat.query.all()
        count_A = Flat.query.filter_by(block="A").count()
        count_B = Flat.query.filter_by(block="B").count()

        expenses_q = Expense.query.filter_by(month=month)
        if scope != "all":
            expenses_q = expenses_q.filter_by(scope=scope)
        total_expense = sum(e.amount for e in expenses_q.all())

        if scope == "A":
            per_flat = total_expense / max(count_A, 1)
            target_flats = Flat.query.filter_by(block="A").all()
        elif scope == "B":
            per_flat = total_expense / max(count_B, 1)
            target_flats = Flat.query.filter_by(block="B").all()
        else:
            per_flat = total_expense / max(len(flats), 1)
            target_flats = flats

        for f in target_flats:
            due = Due.query.filter_by(flat_id=f.id, month=month).first()
            if not due:
                due = Due(flat_id=f.id, month=month)
                db.session.add(due)
            due.total_expense_month = total_expense
            due.per_flat_due = per_flat
            due.balance = due.per_flat_due - due.paid_amount

        db.session.commit()
        flash(f"{month} ayı aidat hesaplandı.", "success")
        return redirect(url_for("dashboard.admin_dashboard"))

    return render_template("dashboard_admin.html")
