from datetime import datetime
from app.services.status_service import rent_status

def auto_suspend_tenant(payment, db):
    status_data = rent_status(payment)

    if status_data["status"] == "overdue":
        tenant = payment.tenant

        if tenant.is_active:
            tenant.is_active = False
            tenant.suspended_at = datetime.utcnow()
            db.commit()
