from pydantic import BaseModel


class Registration(BaseModel):
    login: str
    password: str
    confir_password: str


class Authorization(BaseModel):
    login: str
    password: str


class ChangePassword(BaseModel):
    login: str
    password_old: str
    password_new: str


class DeleteAccount(BaseModel):
    login: int


class ChangeLogin(BaseModel):
    old_login: str
    new_login: str
