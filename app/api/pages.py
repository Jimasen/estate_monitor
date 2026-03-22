from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.page import Page

router = APIRouter()

# Demo fallback
PAGES = {
    "about": {"title": "About Estate Monitor", "content": "Estate Monitor is a platform for property management, investment and marketplace across Africa."},
    "contact": {"title": "Contact Us", "content": "Email: support@estatemonitor.com"},
    "invest": {"title": "Invest in Real Estate", "content": "Join our property investment pool and earn passive income."}
}

@router.get("/page/{slug}")
def get_page(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()
    if page:
        return {"title": page.title, "content": page.content}
    if slug in PAGES:
        return PAGES[slug]
    raise HTTPException(status_code=404, detail="Page not found")

