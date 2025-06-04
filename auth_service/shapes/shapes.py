from pydantic import BaseModel

class Registration(BaseModel):
    login: str
    password: str
    confir_password: str

class Authorization(BaseModel):
    login : str
    password : str