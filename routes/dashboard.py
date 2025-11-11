from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Yönetici dashboard
@dashboard_bp.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403
    return render_template("dashboard_admin.html")

# Sakin dashboard
@dashboard_bp.route("/resident")
@login_required
def resident_dashboard():
    if current_user.role != "resident":
        return render_template("unauthorized.html"), 403
    return render_template("dashboard_resident.html")
