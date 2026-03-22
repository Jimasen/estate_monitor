# app/api/tenant/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate
from app.core.events import emit, TENANT_CREATED, PAYMENT_RECEIVED


router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"]
)


# ======================================
# TENANT DASHBOARD
# ======================================
@router.get("/dashboard")
async def tenant_dashboard(db: Session = Depends(get_db)):
    tenant_count = db.query(Tenant).count()

    return {
        "tenant_count": tenant_count
    }


# ======================================
# TENANT PROFILE
# ======================================
@router.get("/profile/{tenant_id}")
async def tenant_profile(tenant_id: int, db: Session = Depends(get_db)):

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return {
        "id": tenant.id,
        "full_name": tenant.full_name,
        "phone": tenant.phone_number,  # ✅ FIXED
        "property_id": tenant.property_id,
        "created_at": tenant.created_at
    }


# ======================================
# CREATE TENANT
# ======================================
@router.post("/create")
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):

    # ✅ FIXED: use schema field (phone)
    existing = db.query(Tenant).filter(
        Tenant.phone_number == tenant_data.phone
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    # ✅ FIXED: map correctly to DB field
    tenant = Tenant(
        full_name=tenant_data.full_name,
        phone_number=tenant_data.phone,
        property_id=tenant_data.property_id
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    # trigger async events (notifications, logs, etc)
    await emit(TENANT_CREATED, {"tenant": tenant})

    return {
        "message": "Tenant created successfully",
        "tenant_id": tenant.id,
        "phone": tenant.phone_number  # ✅ FIXED
    }


# ======================================
# RECORD PAYMENT
# ======================================
@router.post("/{tenant_id}/payments")
async def record_payment(
    tenant_id: int,
    amount: float,
    db: Session = Depends(get_db)
):

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    # trigger event
    await emit(PAYMENT_RECEIVED, {
        "tenant": tenant,
        "amount": amount
    })

    return {
        "message": "Payment recorded successfully",
        "tenant_id": tenant.id,
        "amount": amount
    }
