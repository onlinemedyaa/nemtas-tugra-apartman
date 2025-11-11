from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Payment, Due, Flat, AuditLog
import os

payments_bp = Blueprint('payments', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

@payments_bp.route("/payments", methods=["GET"])
@login_required
def list_payments():
    q = Payment.query
    if current_user.role == "resident":
        flat = Flat.query.filter(Flat.resident_user_id == current_user.id).first()
        if flat:
            q = q.filter(Payment.flat_id == flat.id)
    items = q.order_by(Payment.date.desc()).all()
    return render_template("payments.html", items=items)

@payments_bp.route("/payments", methods=["POST"])
@login_required
def add_payment():
    amount = float(request.form.get("amount"))
    month = request.form.get("month")
    note = request.form.get("note")
    flat = Flat.query.filter(Flat.resident_user_id == current_user.id).first()
    due = Due.query.filter_by(flat_id=flat.id, month=month).first()
    if not due:
        flash("Önce bu ay için aidatlar oluşturulmalı.", "danger")
        return redirect(url_for("dues.list_dues", month=month))
    p = Payment(due_id=due.id, flat_id=flat.id, amount=amount, note=note)
    db.session.add(p)
    due.paid_amount = round((due.paid_amount or 0) + amount, 2)
    due.balance = round(due.per_flat_due - due.paid_amount, 2)
    db.session.commit()
    db.session.add(AuditLog(user_id=current_user.id, action="create", entity="payment", entity_id=p.id,
                            details=f"{month} ödeme {amount} TL"))
    db.session.commit()
    flash("Ödeme eklendi.", "success")
    return redirect(url_for("payments.list_payments"))

@payments_bp.route("/payments/<int:payment_id>/receipt", methods=["POST"])
@login_required
def upload_receipt(payment_id):
    file = request.files.get("file")
    if not file or not allowed_file(file.filename):
        flash("Geçersiz dosya.", "danger")
        return redirect(url_for("payments.list_payments"))
    filename = f"payment_{payment_id}_{file.filename.replace(' ', '_')}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    pay = Payment.query.get(payment_id)
    pay.receipt_path = filename
    db.session.commit()
    db.session.add(AuditLog(user_id=current_user.id, action="update", entity="payment", entity_id=payment_id,
                            details=f"Dekont: {filename}"))
    db.session.commit()
    flash("Dekont yüklendi.", "success")
    return redirect(url_for("payments.list_payments"))
