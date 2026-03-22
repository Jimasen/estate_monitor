# app/api/public_files.py

from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/invoices/{filename}")
def serve_invoice(filename: str):
    file_path = f"/tmp/{filename}"

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type="application/pdf")
