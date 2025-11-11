from app import app, db
from models import User, Flat
from werkzeug.security import generate_password_hash

def seed():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(phone="5550000000").first()
        if not admin:
            admin = User(phone="5550000000", name="Yönetici", role="admin",
                         pin_hash=generate_password_hash("123456"))
            db.session.add(admin)
        for block, count in [("A", 18), ("B", 17)]:
            for num in range(1, count+1):
                code = f"{block}-{num}"
                if not Flat.query.filter_by(code=code).first():
                    f = Flat(block=block, number=num, code=code)
                    db.session.add(f)
        db.session.commit()
        print("Seed tamamlandı.")

if __name__ == "__main__":
    seed()
