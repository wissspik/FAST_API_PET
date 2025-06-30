from pydantic import BaseModel

class FileUpload(BaseModel):
    user_id: int