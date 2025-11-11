from models import db, Due, Expense, Flat
from sqlalchemy import func

A_COUNT = 18
B_COUNT = 17
ALL_COUNT = A_COUNT + B_COUNT

def generate_dues(month: str):
    # Ayın giderlerini çek
    expenses = Expense.query.filter(Expense.month == month).all()
    total_expense = sum(e.amount for e in expenses)
    # Kişi başı due, scope'a göre hesaplanır
    # Her due satırı, ilgili flat için tüm giderlerin toplam kişi payını içerir
    flats = Flat.query.all()

    for f in flats:
        per_flat_total = 0.0
        for e in expenses:
            if e.scope == "A":
                if f.block == "A":
                    per_flat_total += e.amount / A_COUNT
            elif e.scope == "B":
                if f.block == "B":
                    per_flat_total += e.amount / B_COUNT
            else:
                per_flat_total += e.amount / ALL_COUNT

        per_flat_total = round(per_flat_total, 2)
        due = Due.query.filter_by(flat_id=f.id, month=month).first()
        if not due:
            due = Due(flat_id=f.id, month=month)
            db.session.add(due)
        due.total_expense_month = round(total_expense, 2)
        due.per_flat_due = per_flat_total
        due.balance = round((due.per_flat_due - (due.paid_amount or 0)), 2)

    db.session.commit()
    return {"month": month, "total_expense": round(total_expense, 2)}
