from app.database.session import SessionLocal
from app.models.tenant import Tenant
from app.services.notification_service import send_rent_reminder


def rent_reminder_job():

    db = SessionLocal()

    tenants = db.query(Tenant).all()

    for tenant in tenants:

        send_rent_reminder(tenant)

    db.close()
