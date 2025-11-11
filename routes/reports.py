from flask import Blueprint, render_template, request, send_file, current_app, jsonify
from flask_login import login_required
from services.reports import cash_report, category_breakdown
from services.pdf import generate_month_pdf
from models import Expense, Due, Payment, Flat
import pandas as pd
import os

reports_bp = Blueprint('reports', __name__)

@reports_bp.route("/cash-report", methods=["GET"])
@login_required
def cash_report_page():
    month = request.args.get("month")
    data = cash_report(month) if month else None
    cats = category_breakdown(month) if month else []
    return render_template("cash_report.html", data=data, cats=cats, month=month)

@reports_bp.route("/export/cash-report.csv", methods=["GET"])
@login_required
def export_csv():
    month = request.args.get("month")
    data = cash_report(month)
    df = pd.DataFrame([data])
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"cash_{month}.csv")
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)

@reports_bp.route("/export/cash-report.xlsx", methods=["GET"])
@login_required
def export_excel():
    month = request.args.get("month")
    data = cash_report(month)
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"cash_{month}.xlsx")
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame([data]).to_excel(writer, index=False, sheet_name="Kasa")
        cats = category_breakdown(month)
        pd.DataFrame(cats).to_excel(writer, index=False, sheet_name="Kategoriler")
    return send_file(path, as_attachment=True)

@reports_bp.route("/export/cash-report.pdf", methods=["GET"])
@login_required
def export_pdf():
    month = request.args.get("month")
    filename, path = generate_month_pdf(month, current_app.config.get("APARTMENT_NAME", "Apartman"))
    return send_file(path, as_attachment=True, download_name=filename)

@reports_bp.route("/chart-data", methods=["GET"])
@login_required
def chart_data():
    month = request.args.get("month")
    cats = category_breakdown(month)
    labels = [c["category"] for c in cats]
    values = [c["amount"] for c in cats]
    return jsonify({"labels": labels, "values": values})
