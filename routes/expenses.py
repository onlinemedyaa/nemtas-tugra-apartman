from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from models import db, Expense, AuditLog
import os

expenses_bp = Blueprint('expenses', __name__)

CATEGORIES = ["Elektrik","Bina Temizlik","Çöp Alımı","Asansör Bakım","Su","Ek Tamir Masrafı","Olağan Dışı Gider"]
SCOPES = ["all","A","B"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

@expenses_bp.route("/expenses", methods=["GET"])
@login_required
def list_expenses():
    month = request.args.get("month")
    q = Expense.query
    if month:
        q = q.filter(Expense.month == month)
    items = q.order_by(Expense.date.desc()).all()
    return render_template("expenses.html", items=items, month=month, categories=CATEGORIES, scopes=SCOPES)

@expenses_bp.route("/admin/expenses", methods=["POST"])
@login_required
def add_expense():
    if current_user.role != "admin":
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("expenses.list_expenses"))
    category = request.form.get("category")
    description = request.form.get("description")
    amount = float(request.form.get("amount"))
    month = request.form.get("month")
    scope = request.form.get("scope", "all")
    if category not in CATEGORIES or scope not in SCOPES:
        flash("Geçersiz kategori veya kapsam.", "danger")
        return redirect(url_for("expenses.list_expenses", month=month))
    exp = Expense(category=category, description=description, amount=amount, month=month, scope=scope)
    db.session.add(exp)
    db.session.commit()
    db.session.add(AuditLog(user_id=current_user.id, action="create", entity="expense", entity_id=exp.id,
                            details=f"{month} {category} {amount} TL scope={scope}"))
    db.session.commit()
    flash("Gider eklendi.", "success")
    return redirect(url_for("expenses.list_expenses", month=month))

@expenses_bp.route("/admin/expenses/<int:expense_id>/receipt", methods=["POST"])
@login_required
def upload_receipt(expense_id):
    if current_user.role != "admin":
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("expenses.list_expenses"))
    file = request.files.get("file")
    if not file or not allowed_file(file.filename):
        flash("Geçersiz dosya.", "danger")
        return redirect(url_for("expenses.list_expenses"))
    filename = f"expense_{expense_id}_{file.filename.replace(' ', '_')}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    exp = Expense.query.get(expense_id)
    exp.receipt_path = filename
    db.session.commit()
    flash("Makbuz yüklendi.", "success")
    return redirect(url_for("expenses.list_expenses"))

@expenses_bp.route("/uploads/<path:filename>")
@login_required
def serve_upload(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
