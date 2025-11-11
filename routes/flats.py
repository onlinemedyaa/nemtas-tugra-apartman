from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Flat

flats_bp = Blueprint('flats', __name__)

@flats_bp.route("/my-flat", methods=["GET"])
@login_required
def my_flat():
    flat = Flat.query.filter(Flat.resident_user_id == current_user.id).first()
    return render_template("profile.html", flat=flat)
