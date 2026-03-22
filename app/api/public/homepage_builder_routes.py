from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cms import Block
import shutil

router = APIRouter(
    prefix="/api/homepage-builder",
    tags=["Homepage Builder"]
)

# CREATE BLOCK
@router.post("/blocks")
def create_block(payload: dict, db: Session = Depends(get_db)):
    block = Block(**payload)
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


# REORDER BLOCKS
@router.put("/reorder")
def reorder_blocks(blocks: list, db: Session = Depends(get_db)):
    for item in blocks:
        block = db.query(Block).get(item["id"])
        block.position = item["position"]

    db.commit()
    return {"message": "Layout updated"}


# UPLOAD IMAGE
@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    file_path = f"app/static/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/static/{file.filename}"}
