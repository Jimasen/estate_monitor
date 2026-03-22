from fastapi import APIRouter, Depends
from datetime import datetime

from app.api.deps import get_current_user
from app.core.subscription_guard import require_plan

router = APIRouter()

# -------------------------
# EXECUTIVE DASHBOARD
# -------------------------

@router.get("/executive/overview")
def executive_overview(
    user=Depends(get_current_user),
    _=Depends(require_plan("pro"))
):
    return {
        "status": "active",
        "role": "executive",
        "timestamp": datetime.utcnow().isoformat(),
        "features": [
            "estate_overview",
            "live_payments",
            "tenant_activity",
            "system_alerts",
            "future_insights"
        ]
    }
