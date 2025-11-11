from werkzeug.security import generate_password_hash
from models import db, User, Flat
from app import app
import os
from config import Config

def seed_data():
    with app.app_context():
        # uploads klasörü garanti
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        db.create_all()

        # Yönetici hesabı
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
    seed_data()
