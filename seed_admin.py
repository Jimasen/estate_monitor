# seed_admin.py
from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

email = "admin@estate.com"

if not db.query(User).filter(User.email == email).first():
    admin = User(
        full_name="System Admin",
        email=email,
        password_hash=hash_password("admin123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("✅ Admin created: admin@estate.com / admin123")
else:
    print("ℹ️ Admin already exists")

db.close()

