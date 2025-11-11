from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from models import Expense, Payment, Due, Flat
from services.reports import cash_report, category_breakdown
from flask import current_app
import os

def generate_month_pdf(month: str, apartment_name: str):
    # Dosya yolu
    filename = f"report_{month}.pdf"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    story = []

    # Başlık
    story.append(Paragraph(f"<b>{apartment_name}</b>", styles['Title']))
    story.append(Paragraph(f"{month} Kasa Raporu", styles['h2']))
    story.append(Spacer(1, 8))

    # Kasa özeti
    cash = cash_report(month)
    summary_data = [
        ["Toplam Gelir (TL)", f"{cash['total_income']:.2f}"],
        ["Toplam Gider (TL)", f"{cash['total_expense']:.2f}"],
        ["Kasa Bakiye (TL)", f"{cash['cash_balance']:.2f}"],
    ]
    t = Table(summary_data, colWidths=[100*mm, 60*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Kategori dağılımı
    story.append(Paragraph("Gider Kategori Dağılımı", styles['h3']))
    cats = category_breakdown(month)
    cat_table = [["Kategori", "Tutar (TL)"]] + [[c["category"], f"{c['amount']:.2f}"] for c in cats]
    ct = Table(cat_table, colWidths=[100*mm, 60*mm])
    ct.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    story.append(ct)
    story.append(Spacer(1, 12))

    # Aidat listesi (daire bazlı)
    story.append(Paragraph("Aidat Listesi", styles['h3']))
    dues = Due.query.filter(Due.month == month).order_by(Due.flat_id.asc()).all()
    rows = [["Daire", "Kişi Başı Aidat", "Ödenen", "Kalan"]] + [
        [Flat.query.get(d.flat_id).code, f"{d.per_flat_due:.2f}", f"{(d.paid_amount or 0):.2f}", f"{(d.balance or 0):.2f}"]
        for d in dues
    ]
    dt = Table(rows, colWidths=[40*mm, 40*mm, 40*mm, 40*mm])
    dt.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    story.append(dt)
    story.append(Spacer(1, 12))

    # Ödemeler listesi
    story.append(Paragraph("Ödemeler", styles['h3']))
    pays = Payment.query.filter(Payment.date.like(f"{month}%")).order_by(Payment.date.desc()).all()
    pay_rows = [["Tarih", "Daire", "Tutar", "Not"]] + [
        [str(p.date)[:10], Flat.query.get(p.flat_id).code, f"{p.amount:.2f}", p.note or ""]
        for p in pays
    ]
    pt = Table(pay_rows, colWidths=[35*mm, 35*mm, 35*mm, 65*mm])
    pt.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    story.append(pt)

    doc.build(story)
    return filename, path
