from werkzeug.security import generate_password_hash
from models import db, User, Flat
from app import app

def seed_data():
    with app.app_context():
        # Tabloları oluştur
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

        # A blok daireleri (1-18)
        for i in range(1, 19):
            if not Flat.query.filter_by(block="A", number=i).first():
                flat = Flat(block="A", number=i)
                db.session.add(flat)

        # B blok daireleri (1-17)
        for i in range(1, 18):
            if not Flat.query.filter_by(block="B", number=i).first():
                flat = Flat(block="B", number=i)
                db.session.add(flat)

        db.session.commit()
        print("Seed işlemi tamamlandı: Yönetici ve daireler eklendi.")

if __name__ == "__main__":
    seed_data()
