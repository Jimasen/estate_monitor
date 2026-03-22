from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.property import Property
from app.models.property_sale import PropertySale

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])


@router.get("/properties")
def list_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()


@router.get("/sales")
def properties_for_sale(db: Session = Depends(get_db)):
    return db.query(PropertySale).all()

