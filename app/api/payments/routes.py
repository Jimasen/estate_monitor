from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database.session import get_db
from app.models.payment import RentPayment
from app.models.tenant import Tenant

router = APIRouter()


@router.post("/api/pay")
def create_payment(
    tenant_id: int,
    amount: float,
    db: Session = Depends(get_db)
):
    # ✅ Validate tenant
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # ✅ Generate reference
    reference = str(uuid.uuid4())

    # ✅ Create payment
    payment = RentPayment(
        tenant_id=tenant.id,
        amount=amount,
        status="pending",
        due_date=datetime.utcnow(),  # you can improve this later
        gateway="paystack",          # or flutterwave later
        reference=reference
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.id,
        "reference": payment.reference,
        "amount": payment.amount,
        "status": payment.status
    }


@router.get("/api/receipts/{payment_id}")
def download_receipt(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(RentPayment).filter(RentPayment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {
        "payment_id": payment.id,
        "tenant_id": payment.tenant_id,
        "amount": payment.amount,
        "status": payment.status,
        "reference": payment.reference,
        "paid_at": payment.paid_at
    }
