from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Expense, Payment, Due, Flat

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/cash")
@login_required
def cash_report():
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403

    total_expenses = sum(e.amount for e in Expense.query.all())
    total_payments = sum(p.amount for p in Payment.query.all())
    total_balance = sum(d.balance for d in Due.query.all())
    flats_count = Flat.query.count()

    return render_template(
        "dashboard_admin.html",
        total_expenses=total_expenses,
        total_payments=total_payments,
        total_balance=total_balance,
        flats_count=flats_count
    )
