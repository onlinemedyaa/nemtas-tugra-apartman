from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="resident")  # admin | resident
    pin_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(1), nullable=False)  # A | B
    number = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    owner_name = db.Column(db.String(100))
    tenant_name = db.Column(db.String(100))
    resident_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone = db.Column(db.String(20))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today)
    month = db.Column(db.String(7), nullable=False)  # YYYY-MM
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    scope = db.Column(db.String(2), default="all")  # all | A | B
    receipt_path = db.Column(db.String(255))

class Due(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    total_expense_month = db.Column(db.Float, default=0)
    per_flat_due = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float, default=0)
    balance = db.Column(db.Float, default=0)
    last_payment_date = db.Column(db.DateTime)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_id = db.Column(db.Integer, db.ForeignKey('due.id'), nullable=False)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(255))
    receipt_path = db.Column(db.String(255))

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(50))  # create|update|delete
    entity = db.Column(db.String(50))  # expense|payment|due|flat|user
    entity_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(255))
