from fastapi import WebSocket
from typing import Dict, List

# tenant_id -> user_id -> connections
active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}

async def connect(websocket: WebSocket, tenant_id: int, user_id: int):
    if tenant_id not in active_connections:
        active_connections[tenant_id] = {}

    if user_id not in active_connections[tenant_id]:
        active_connections[tenant_id][user_id] = []

    active_connections[tenant_id][user_id].append(websocket)

async def disconnect(websocket: WebSocket, tenant_id: int, user_id: int):
    active_connections[tenant_id][user_id].remove(websocket)

    if not active_connections[tenant_id][user_id]:
        del active_connections[tenant_id][user_id]

    if not active_connections[tenant_id]:
        del active_connections[tenant_id]

async def broadcast_to_tenant(tenant_id: int, message: dict):
    if tenant_id in active_connections:
        for users in active_connections[tenant_id].values():
            for connection in users:
                await connection.send_json(message)

async def send_to_user(tenant_id: int, user_id: int, message: dict):
    if tenant_id in active_connections:
        if user_id in active_connections[tenant_id]:
            for connection in active_connections[tenant_id][user_id]:
                await connection.send_json(message)

# ✅ ADD THIS FUNCTION
async def broadcast(tenant_id: int, message: dict):
    await broadcast_to_tenant(tenant_id, message)
