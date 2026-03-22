from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.payment_service import confirm_payment

router = APIRouter(prefix="/api/billing", tags=["Billing"])


@router.post("/webhook/flutterwave")
async def flutterwave_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    data = payload.get("data", {})
    status = data.get("status")

    if status != "successful":
        return {"status": "ignored"}

    reference = data.get("tx_ref")
    amount = float(data.get("amount", 0))

    confirm_payment(db, reference, amount)

    return {"status": "ok"}
