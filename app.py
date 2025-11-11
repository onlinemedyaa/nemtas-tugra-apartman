from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

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

# Veritabanı başlatma
db.init_app(app)

# Login Manager ayarları
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

# Ana çalıştırma
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # Tabloları oluşturur
    app.run(host="0.0.0.0", port=5000, debug=True)
