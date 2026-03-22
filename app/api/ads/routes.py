# app/api/ads/routes.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.models.property import PropertyAd, PropertyAdMedia
from app.schemas import PropertyAdCreate
from app.api.auth.deps import get_current_user
from app.database.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/ads", tags=["Ads & Media"])

@router.post("/", response_model=PropertyAdCreate)
def create_ad():
    ...

@router.get("/")
def list_ads(db: Session = Depends(get_db)):
    ...

# Directory for uploaded media
MEDIA_DIR = Path(__file__).parent.parent.parent / "static" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# PROPERTY ADS
# -------------------------
@router.post("/ads", response_model=PropertyAdCreate)
def create_ad(
    ad: PropertyAdCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new property ad (only logged-in users).
    """
    new_ad = PropertyAd(**ad.dict(), created_by=current_user.id)
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return new_ad

@router.get("/ads", response_model=List[PropertyAdCreate])
def list_ads(db: Session = Depends(get_db)):
    """
    List all approved property ads.
    """
    return db.query(PropertyAd).filter_by(is_approved=True).all()

# -------------------------
# USER MEDIA (IMAGES / FILES)
# -------------------------
@router.post("/media")
def upload_media(
    file: UploadFile = File(...),
    media_type: str = "image",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload user media for ads (images/videos).
    """
    file_path = MEDIA_DIR / file.filename
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    media = PropertyAdMedia(
        user_id=current_user.id,
        file_url=f"/static/media/{file.filename}",
        media_type=media_type,
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

@router.get("/media/{user_id}")
def get_user_media(user_id: int, db: Session = Depends(get_db)):
    """
    Return all media uploaded by a specific user.
    """
    media_list = db.query(PropertyAdMedia).filter_by(user_id=user_id).all()
    return [
        {
            "id": m.id,
            "file_url": m.file_url,
            "media_type": m.media_type
        } for m in media_list
    ]


