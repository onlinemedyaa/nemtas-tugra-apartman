from models import db, Expense, Payment
from sqlalchemy import func

def cash_report(month: str):
    total_expense = db.session.query(func.coalesce(func.sum(Expense.amount), 0))\
        .filter(Expense.month == month).scalar()
    total_income = db.session.query(func.coalesce(func.sum(Payment.amount), 0))\
        .filter(func.strftime('%Y-%m', Payment.date) == month).scalar()
    return {
        "month": month,
        "total_expense": round(total_expense, 2),
        "total_income": round(total_income, 2),
        "cash_balance": round(total_income - total_expense, 2)
    }

def category_breakdown(month: str):
    rows = db.session.query(Expense.category, func.sum(Expense.amount))\
        .filter(Expense.month == month).group_by(Expense.category).all()
    return [{"category": c, "amount": float(a)} for c, a in rows]
