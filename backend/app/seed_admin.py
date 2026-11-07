from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password

# Run: python -m app.seed_admin
db = SessionLocal()
try:
    email = "admin@clinic.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        db.add(User(name="Clinic Admin", email=email, password_hash=hash_password("Admin12345!"), role="admin"))
        db.commit()
        print("Admin created: admin@clinic.com / Admin12345!")
    else:
        print("Admin already exists")
finally:
    db.close()
