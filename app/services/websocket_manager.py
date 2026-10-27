from typing import Dict, List
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str = "global"):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str = "global"):
        if channel in self.active_connections and websocket in self.active_connections[channel]:
            self.active_connections[channel].remove(websocket)

    async def broadcast_to_channel(self, channel: str, message: dict):
        if channel in self.active_connections:
            for connection in list(self.active_connections[channel]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, channel)


ws_manager = WebSocketManager()
