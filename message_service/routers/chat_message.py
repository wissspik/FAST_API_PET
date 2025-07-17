from fastapi import APIRouter,WebSocket, WebSocketDisconnect

from message_service.database.db import get_database

from message_service.shapes.shapes import MessageIn

app = APIRouter()
