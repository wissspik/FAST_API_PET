from pydantic import BaseModel

class FileUpload(BaseModel):
    file: bytes
    user_id: int