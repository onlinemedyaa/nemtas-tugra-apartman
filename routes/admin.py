from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, Flat

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/users")
@login_required
def users_admin():
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403
    users = User.query.all()
    flats = Flat.query.all()
    return render_template("dashboard_admin.html", users=users, flats=flats)
