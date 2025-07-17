from pydantic import BaseModel

from datetime import datetime


class MessageIn(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageOut(MessageIn):
    id: str
    timestamp: datetime