from pydantic import BaseModel, SecretStr, Field, field_validator
class Registration(BaseModel):
    login: str
    password: str = Field(min_length=12, max_length=36)
