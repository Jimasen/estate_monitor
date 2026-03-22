from database import SessionLocal
from models import User, RentPayment
from auth import hash_password

db = SessionLocal()

# --- ADMIN ---
admin = User(
    email="admin@estate.com",
    password=hash_password("admin123"),
    role="admin",
)

# --- TENANT ---
tenant = User(
    email="tenant@estate.com",
    password=hash_password("tenant123"),
    role="tenant",
)

db.add_all([admin, tenant])
db.commit()

# --- RENT PAYMENTS ---
rent1 = RentPayment(
    tenant_id=tenant.id,
    amount_due=150000,
    due_date="2026-02-15",
    status="pending",
)

rent2 = RentPayment(
    tenant_id=tenant.id,
    amount_due=200000,
    due_date="2026-03-15",
    status="pending",
)

db.add_all([rent1, rent2])
db.commit()

print("✅ Admin & Tenant seeded successfully")
