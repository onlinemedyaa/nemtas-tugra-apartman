from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from models import db
from config import Config

# Blueprint'leri içe aktar
from routes.auth import auth_bp, login_manager
from routes.expenses import expenses_bp
from routes.dues import dues_bp
from routes.payments import payments_bp
from routes.flats import flats_bp
from routes.reports import reports_bp
from routes.admin import admin_bp

import os

# Flask uygulaması
app = Flask(__name__)
app.config.from_object(Config)

# Veritabanı başlat
db.init_app(app)

# Login manager başlat
login_manager.init_app(app)

# Upload klasörü oluştur
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Ana sayfa yönlendirmesi
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.role == "admin":
        return render_template("dashboard_admin.html")
    return render_template("dashboard_resident.html")

# Blueprint kayıtları
app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(dues_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(flats_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(admin_bp)

# Çalıştırma
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
