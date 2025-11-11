from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db, Expense
from config import Config

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

# Giderleri listeleme
@expenses_bp.route("/")
@login_required
def list_expenses():
    if current_user.role != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("dashboard.resident_dashboard"))

    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("expenses.html", expenses=expenses)

# Yeni gider ekleme
@expenses_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if current_user.role != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("dashboard.resident_dashboard"))

    if request.method == "POST":
        category = request.form.get("category")
        description = request.form.get("description")
        amount = float(request.form.get("amount"))
        month = request.form.get("month")
        scope = request.form.get("scope")

        # Makbuz yükleme
        receipt = request.files.get("receipt")
        receipt_path = None
        if receipt and receipt.filename != "":
            filename = secure_filename(receipt.filename)
            receipt_path = os.path.join("uploads", filename)
            receipt.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        expense = Expense(
            category=category,
            description=description,
            amount=amount,
            month=month,
            scope=scope,
            receipt_path=receipt_path
        )
        db.session.add(expense)
        db.session.commit()

        flash("Gider başarıyla eklendi.", "success")
        return redirect(url_for("expenses.list_expenses"))

    return render_template("add_expense.html")
