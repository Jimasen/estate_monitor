import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from app.services.status_service import subscription_status, rent_status
from app.database.session import SessionLocal
from app.models.user import User
from app.models.payment import RentPayment

class StatusConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_status(self, websocket: WebSocket, user_id: int):
        db = SessionLocal()

        user = db.query(User).filter(User.id == user_id).first()
        rent = db.query(RentPayment).filter(
            RentPayment.user_id == user_id
        ).order_by(RentPayment.due_date.desc()).first()

        payload = {
            "subscription": subscription_status(user),
            "rent": rent_status(rent) if rent else {
                "color": "grey",
                "blink": "none",
                "progress": 0.0
            }
        }

        await websocket.send_text(json.dumps(payload))
        db.close()

manager = StatusConnectionManager()


async def status_ws(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)

    try:
        while True:
            await manager.send_status(websocket, user_id)
            await asyncio.sleep(5)  # 🔁 push every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
