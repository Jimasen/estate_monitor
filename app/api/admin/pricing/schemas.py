from pydantic import BaseModel
from typing import Optional, Dict

# -------------------------------
# Input schema to create pricing
# -------------------------------
class CountryPricingCreate(BaseModel):
    country_id: int
    plan_id: int
    monthly_price: float
    yearly_price: float
    promo_price: Optional[float] = None
    trial_days: int = 0
    active: bool = True


# -------------------------------
# Update schema (partial updates)
# -------------------------------
class PricingUpdate(BaseModel):
    country_code: str
    plan_name: str
    monthly_price: Optional[float] = None
    yearly_price: Optional[float] = None
    promo_price: Optional[float] = None
    trial_days: Optional[int] = None
    active: Optional[bool] = None


# -------------------------------
# Output schema
# -------------------------------
class CountryPricingOut(BaseModel):
    id: int
    country: Dict
    plan: Dict
    monthly_price: float
    yearly_price: float
    promo_price: Optional[float] = None
    trial_days: int
    active: bool

    class Config:
        orm_mode = True

