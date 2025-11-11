import os

class Config:
    # Flask gizli anahtar (CSRF, session için)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"

    # SQLite veritabanı dosyası
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "apartman.db")

    # SQLAlchemy ayarları
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload klasörü
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

    # Debug modu (Render’da kapalı, yerelde açık olabilir)
    DEBUG = True
