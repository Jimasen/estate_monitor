# app/api/websocket_routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket.status_socket import connect, disconnect
from app.api.auth.dependencies import get_current_user
from app.database.session import SessionLocal
from app.models.user import User

router = APIRouter()


@router.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):

    # Access session from websocket
    await websocket.accept()

    session = websocket.scope.get("session")

    if not session or "user_id" not in session:
        await websocket.close(code=1008)
        return

    db = SessionLocal()
    user = db.query(User).filter(User.id == session["user_id"]).first()

    if not user:
        await websocket.close(code=1008)
        return

    tenant_id = user.tenant_id

    await connect(websocket, tenant_id, user.id)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await disconnect(websocket, tenant_id, user.id)
