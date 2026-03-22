# app/api/admin/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.property import PropertyAd
from app.models.user_media import UserMedia
from app.models.user import User
from app.api.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# -------------------------
# ADMIN GUARD
# -------------------------
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


# -------------------------
# PROPERTY ADS
# -------------------------
@router.get("/ads/pending", response_model=List[dict])
def list_pending_ads(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    ads = db.query(PropertyAd).filter(PropertyAd.is_approved == False).all()
    return [
        {
            "id": ad.id,
            "title": ad.title,
            "owner": ad.owner_name,
        }
        for ad in ads
    ]


@router.post("/ads/{ad_id}/approve")
def approve_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    ad = db.query(PropertyAd).filter(PropertyAd.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    ad.is_approved = True
    db.commit()
    return {"message": "Ad approved"}


@router.post("/ads/{ad_id}/reject")
def reject_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    ad = db.query(PropertyAd).filter(PropertyAd.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    db.delete(ad)
    db.commit()
    return {"message": "Ad rejected"}


# -------------------------
# USER MEDIA
# -------------------------
@router.get("/media/pending", response_model=List[dict])
def list_pending_media(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    media = db.query(UserMedia).filter(UserMedia.is_approved == False).all()
    return [
        {
            "id": m.id,
            "name": m.filename,
            "uploader": m.uploader_name,
        }
        for m in media
    ]


@router.post("/media/{media_id}/approve")
def approve_media(
    media_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    media = db.query(UserMedia).filter(UserMedia.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    media.is_approved = True
    db.commit()
    return {"message": "Media approved"}


@router.post("/media/{media_id}/reject")
def reject_media(
    media_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    media = db.query(UserMedia).filter(UserMedia.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    db.delete(media)
    db.commit()
    return {"message": "Media rejected"}
