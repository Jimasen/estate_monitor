# app/api/admin/ads_media.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.property import PropertyAd
from app.models.user_media import UserMedia
from app.api.auth.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

# ----- Approve a property ad -----
@router.post("/ads/{ad_id}/approve")
def approve_ad(ad_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    ad = db.query(PropertyAd).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad.is_approved = True
    db.commit()
    db.refresh(ad)
    return ad

# ----- Approve a media -----
@router.post("/media/{media_id}/approve")
def approve_media(media_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    media = db.query(UserMedia).filter_by(id=media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    media.is_approved = True
    db.commit()
    db.refresh(media)
    return media
