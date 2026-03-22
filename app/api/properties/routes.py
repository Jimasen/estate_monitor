# app/api/properties/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.property import Property

router = APIRouter()

@router.get("/api/properties")
def list_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    return {"properties": [p.name for p in properties]}
