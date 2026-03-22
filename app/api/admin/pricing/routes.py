from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from .schemas import (
    CountryPricingCreate,
    CountryPricingOut,
    PricingUpdate,
)
from .services import (
    create_pricing,
    get_pricing_list,
    update_pricing,
)

router = APIRouter(
    prefix="/admin/pricing",
    tags=["Admin Pricing"],
)

# -------------------------------
# Create new pricing
# -------------------------------
@router.post("/", response_model=CountryPricingOut)
def add_pricing(
    pricing: CountryPricingCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_pricing(db, pricing)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# List all pricing
# -------------------------------
@router.get("/", response_model=List[CountryPricingOut])
def list_pricing(
    db: Session = Depends(get_db),
):
    return get_pricing_list(db)


# -------------------------------
# Update pricing
# -------------------------------
@router.put("/", response_model=dict)
def update_price(
    data: PricingUpdate,
    db: Session = Depends(get_db),
):
    result = update_pricing(db, data)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Country or Plan not found",
        )

    return {"status": "success"}
