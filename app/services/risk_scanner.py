from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.services.risk_analysis_service import calculate_tenant_risk


def scan_all_tenants(db: Session):

    tenants = db.query(Tenant).yield_per(100)

    for tenant in tenants:

        score = calculate_tenant_risk(db, tenant)

        if score > 0.7:
            print(f"⚠ High risk tenant detected: {tenant.id}")
