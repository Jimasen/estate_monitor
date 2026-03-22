from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cms import Page, Block

router = APIRouter(
    prefix="/api/pages",
    tags=["Pages"]
)

# CREATE PAGE
@router.post("/")
def create_page(payload: dict, db: Session = Depends(get_db)):
    page = Page(**payload)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


# GET PAGE WITH BLOCKS
@router.get("/{slug}")
def get_page(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()

    if not page:
        return {"error": "Page not found"}

    blocks = (
        db.query(Block)
        .filter(Block.page_id == page.id)
        .order_by(Block.position)
        .all()
    )

    return {
        "page": page.name,
        "blocks": [
            {
                "type": b.type,
                "config": b.config,
            }
            for b in blocks
        ]
    }
