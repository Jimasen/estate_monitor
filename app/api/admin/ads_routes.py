# app/api/admin/ads_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.property import PropertyAd
from app.models.user_media import UserMedia
from app.models.user import User
from app.schemas.property import PropertyAdSchema, UserMediaSchema
from app.api.auth.dependencies import get_current_user, get_db

router = APIRouter(tags=["Admin Ads & Media"])

# ----- Admin-only check -----
def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ----- List pending ads -----
@router.get("/ads/pending", response_model=List[PropertyAdSchema])
def list_pending_ads(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(PropertyAd).filter_by(is_approved=False).all()

# ----- Approve an ad -----
@router.post("/ads/{ad_id}/approve", response_model=PropertyAdSchema)
def approve_ad(ad_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    ad = db.query(PropertyAd).get(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad.is_approved = True
    db.commit()
    db.refresh(ad)
    return ad

# ----- Reject an ad (delete) -----
@router.delete("/ads/{ad_id}")
def reject_ad(ad_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    ad = db.query(PropertyAd).get(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    db.delete(ad)
    db.commit()
    return {"detail": "Ad rejected and deleted"}

# ----- List pending media -----
@router.get("/media/pending", response_model=List[UserMediaSchema])
def list_pending_media(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(UserMedia).filter_by(is_approved=False).all()

# ----- Approve a media -----
@router.post("/media/{media_id}/approve", response_model=UserMediaSchema)
def approve_media(media_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    media = db.query(UserMedia).get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    media.is_approved = True
    db.commit()
    db.refresh(media)
    return media

# ----- Reject a media (delete) -----
@router.delete("/media/{media_id}")
def reject_media(media_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    media = db.query(UserMedia).get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    db.delete(media)
    db.commit()
    return {"detail": "Media rejected and deleted"}
