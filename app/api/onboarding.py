from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import hash_password

router = APIRouter(prefix="/onboarding", tags=["Tenant Onboarding"])


@router.post("/create")
def create_tenant(
    company_name: str,
    admin_email: str,
    admin_password: str,
    db: Session = Depends(get_db)
):

    tenant = Tenant(name=company_name)

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    admin = User(
        email=admin_email,
        password=hash_password(admin_password),
        role="tenant_admin",
        tenant_id=tenant.id
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Tenant created successfully",
        "tenant_id": tenant.id
    }
