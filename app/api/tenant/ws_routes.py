from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database.session import get_db
from app.models.subscription import Subscription
from app.models.payment import RentPayment
from app.core.security import get_current_user_ws

router = APIRouter()

@router.websocket("/ws/tenant/status")
async def tenant_status_ws(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_ws),
):
    await websocket.accept()

    try:
        while True:
            today = date.today()

            # ------------------
            # Subscription
            # ------------------
            sub = (
                db.query(Subscription)
                .filter(Subscription.user_id == user.id)
                .first()
            )

            subscription_color = "red"
            subscription_blink = "fast"

            if sub and sub.is_active:
                days_left = (sub.expires_at.date() - today).days
                if days_left > 7:
                    subscription_color = "green"
                    subscription_blink = "none"
                elif 0 <= days_left <= 7:
                    subscription_color = "yellow"
                    subscription_blink = "slow"

            # ------------------
            # Rent
            # ------------------
            rent_color = "green"
            rent_blink = "none"

            rents = (
                db.query(RentPayment)
                .filter(RentPayment.tenant_id == user.id)
                .all()
            )

            for r in rents:
                if r.status != "paid" and r.due_date:
                    if r.due_date < today:
                        rent_color = "red"
                        rent_blink = "fast"
                        break
                    elif (r.due_date - today).days <= 5:
                        rent_color = "yellow"
                        rent_blink = "slow"

            await websocket.send_json({
                "subscription": {
                    "color": subscription_color,
                    "blink": subscription_blink
                },
                "rent": {
                    "color": rent_color,
                    "blink": rent_blink
                }
            })

            await websocket.receive_text()

    except WebSocketDisconnect:
        pass
