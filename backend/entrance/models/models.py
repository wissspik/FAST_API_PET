from pydantic import BaseModel

class Registration(BaseModel):
    username: str
    first_password: str
    second_password: str