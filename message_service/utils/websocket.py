from fastapi import WebSocket,WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Dict
from message_service.shapes.shapes import MessageIn


class Connection:
    def __init__(self):
        self.active_connections: Dict[str,WebSocket] = {}
