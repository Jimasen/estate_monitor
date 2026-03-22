from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.app_settings import AppSettings

router = APIRouter(prefix="/settings", tags=["App Settings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get app settings
@router.get("/")
def get_settings(db: Session = Depends(get_db)):
    return db.query(AppSettings).first()

# Update app settings
@router.put("/")
def update_settings(app_name: str = None, logo_url: str = None, primary_color: str = None, db: Session = Depends(get_db)):
    settings = db.query(AppSettings).first()
    if not settings:
        settings = AppSettings()
        db.add(settings)

    if app_name: settings.app_name = app_name
    if logo_url: settings.logo_url = logo_url
    if primary_color: settings.primary_color = primary_color

    db.commit()
    db.refresh(settings)
    return settings
