

# app/schemas/payment.py
from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    tenant_id: int
    property_id: int
    amount_due: float
    amount_paid: float
    tenant_email: str

class PaymentOut(BaseModel):
    id: int
    tenant_id: int
    property_id: int
    amount_due: float
    amount_paid: float
    tenant_email: str
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2
