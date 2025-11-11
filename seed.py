from models import db, User, Flat
from werkzeug.security import generate_password_hash
from app import app

def seed_data():
    with app.app_context():
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

        # Daireler (A ve B blok)
        flats = []
        for i in range(1, 19):  # A blok 18 daire
            flats.append(Flat(block="A", number=i))
        for i in range(1, 18):  # B blok 17 daire
            flats.append(Flat(block="B", number=i))

        for f in flats:
            exists = Flat.query.filter_by(block=f.block, number=f.number).first()
            if not exists:
                db.session.add(f)

        db.session.commit()
        print("Seed işlemi tamamlandı.")

if __name__ == "__main__":
    seed_data()
