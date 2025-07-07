from pydantic import BaseModel

class FileUpload(BaseModel):
    user_id: int

class ChangeProfile(BaseModel):
    user_id: int
    name: str
    surname: str
    patronymic: str
    gender: str # На фронте должно быть только 3 варианта
    city: str
    age: int
