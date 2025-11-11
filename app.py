from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User, Flat
from werkzeug.security import generate_password_hash

# Blueprint importları
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.expenses import expenses_bp
from routes.dues import dues_bp
from routes.payments import payments_bp
from routes.reports import reports_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

# Veritabanı
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Blueprint kayıtları
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(dues_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(admin_bp)

# İlk çalıştırmada tablolar ve seed otomatik
with app.app_context():
    db.create_all()

    # Yönetici hesabı ekle
    if not User.query.filter_by(phone="5550000000").first():
        admin = User(
            phone="5550000000",
            name="Yönetici",
            role="admin",
            pin_hash=generate_password_hash("123456")
        )
        db.session.add(admin)

    # A blok 1-18
    for i in range(1, 19):
        if not Flat.query.filter_by(block="A", number=i).first():
            db.session.add(Flat(block="A", number=i))

    # B blok 1-17
    for i in range(1, 18):
        if not Flat.query.filter_by(block="B", number=i).first():
            db.session.add(Flat(block="B", number=i))

    db.session.commit()
    print("Seed tamamlandı: Yönetici ve daireler eklendi.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
