from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UtilityBillBase(BaseModel):
    estate_id: int
    type: str
    amount_due: float
    due_date: datetime
    status: Optional[str] = "pending"


class UtilityBillCreate(UtilityBillBase):
    pass


class UtilityBillUpdate(BaseModel):
    type: Optional[str]
    amount_due: Optional[float]
    due_date: Optional[datetime]
    status: Optional[str]


class UtilityBillOut(UtilityBillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
