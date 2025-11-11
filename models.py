from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Kullanıcı tablosu
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "admin" veya "resident"
    pin_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler
    flats = db.relationship("Flat", backref="owner", lazy=True)
    payments = db.relationship("Payment", backref="user", lazy=True)

# Daire tablosu
class Flat(db.Model):
    __tablename__ = "flat"
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(1), nullable=False)  # "A" veya "B"
    number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    dues = db.relationship("Due", backref="flat", lazy=True)

# Gider tablosu
class Expense(db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # "YYYY-MM"
    scope = db.Column(db.String(10), default="all")  # "all", "A", "B"
    date = db.Column(db.DateTime, default=datetime.utcnow)
    receipt_path = db.Column(db.String(200))

# Aidat tablosu
class Due(db.Model):
    __tablename__ = "due"
    id = db.Column(db.Integer, primary_key=True)
    flat_id = db.Column(db.Integer, db.ForeignKey("flat.id"), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    total_expense_month = db.Column(db.Float, default=0.0)
    per_flat_due = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)

# Ödeme tablosu
class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    receipt_path = db.Column(db.String(200))

# Audit Log (işlem kayıtları)
class AuditLog(db.Model):
    __tablename__ = "audit_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # create, update, delete
    entity = db.Column(db.String(50), nullable=False)  # expense, payment, due
    entity_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
