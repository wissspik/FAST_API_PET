from pydantic import BaseModel

class Registration(BaseModel):
    login: str
    password: str
    confir_password: str

class Authorization(BaseModel):
    login : str
    password : str

class ChangePassword(BaseModel):
    id : int
    password_old : str
    password_new : str

class DeleteAccount(BaseModel):
    id : str

class ChangeLogin(BaseModel):
    id : int
