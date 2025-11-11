from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Expense
from config import Config
import os

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/")
@login_required
def list_expenses():
    if current_user.role != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("dashboard.resident_dashboard"))
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("expenses.html", expenses=expenses)

@expenses_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if current_user.role != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("dashboard.resident_dashboard"))

    if request.method == "POST":
        category = request.form.get("category")
        description = request.form.get("description")
        amount = float(request.form.get("amount") or 0)
        month = request.form.get("month")
        scope = request.form.get("scope") or "all"

        receipt = request.files.get("receipt")
        receipt_path = None
        if receipt and receipt.filename:
            filename = secure_filename(receipt.filename)
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            file_abs = os.path.join(Config.UPLOAD_FOLDER, filename)
            receipt.save(file_abs)
            receipt_path = os.path.join("uploads", filename)

        exp = Expense(
            category=category,
            description=description,
            amount=amount,
            month=month,
            scope=scope,
            receipt_path=receipt_path
        )
        db.session.add(exp)
        db.session.commit()
        flash("Gider eklendi.", "success")
        return redirect(url_for("expenses.list_expenses"))

    return render_template("add_expense.html")
