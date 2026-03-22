# app/api/ws/routes.py
from fastapi import APIRouter, WebSocket
from app.websocket.ws_manager import manager

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()  # optional echo or ignore
    except Exception:
        await manager.disconnect(websocket)
