# app/api/admin/views.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.security import get_current_user, require_role

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/dashboard")
async def admin_dashboard(request: Request, user = Depends(require_role("admin"))):
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "user": user}
    )
