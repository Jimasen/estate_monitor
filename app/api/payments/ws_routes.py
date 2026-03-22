from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from app.services.payments.flutterwave_service import create_payment as flutterwave_create_payment

router = APIRouter()

# -----------------------------
# WebSocket Manager
# -----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """
        Sends message to all connected clients.
        """
        for connection in self.active_connections:
            await connection.send_json(message)


# Singleton manager
manager = ConnectionManager()

# -----------------------------
# WebSocket Endpoint
# -----------------------------
@router.websocket("/api/payments/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    """
    Owner dashboard listens here for real-time payment updates.
    """
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
