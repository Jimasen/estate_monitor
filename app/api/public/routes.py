# app/api/public/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.property import PropertyAd
from app.models.user_media import UserMedia

router = APIRouter(prefix="/api/public", tags=["Public"])


# ---------- Approved Property Ads ----------
@router.get("/ads", response_model=List[dict])
def get_approved_ads(db: Session = Depends(get_db)):
    ads = (
        db.query(PropertyAd)
        .filter(PropertyAd.is_approved == True)
        .all()
    )

    return [
        {
            "id": ad.id,
            "title": ad.title,
            "description": ad.description,
            "price": ad.price,
            "location": ad.location,
            "image": ad.cover_image,
        }
        for ad in ads
    ]


# ---------- Approved Media ----------
@router.get("/media", response_model=List[dict])
def get_approved_media(db: Session = Depends(get_db)):
    media = (
        db.query(UserMedia)
        .filter(UserMedia.is_approved == True)
        .all()
    )

    return [
        {
            "id": m.id,
            "type": m.media_type,
            "url": m.file_url,
            "owner": m.uploader_name,
        }
        for m in media
    ]
