from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

class Registration(BaseModel):
    login: str
    first_password: str
    second_password: str
class Entrance(BaseModel):
    login: str
    password: str


class Refresh(BaseModel):
    refresh: str


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    content: str = Field(min_length=1, max_length=1500)
    interests: List[str] = Field(min_length=1)


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=256)
    content: Optional[str] = Field(default=None, max_length=1500)
    interests: Optional[List[str]] = None


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    interests: List[str]
    created_at: datetime


class CommentCreate(BaseModel):
    article_id: int
    content: str = Field(min_length=1, max_length=1000)


class CommentOut(BaseModel):
    id: int
    article_id: int
    user_id: int
    content: str
    created_at: datetime


class LikeOut(BaseModel):
    id: int
    article_id: int
    user_id: int
    created_at: datetime


class LikeCount(BaseModel):
    article_id: int
    count: int


class ViewOut(BaseModel):
    id: int
    article_id: int
    user_id: int
    viewed_at: datetime


class ViewCount(BaseModel):
    article_id: int
    count: int


class ProfileUpdate(BaseModel):
    email: Optional[str] = Field(default=None, max_length=120)
    phone: Optional[str] = Field(default=None, max_length=11)


class ProfileOut(BaseModel):
    login: str
    email: Optional[str]
    phone: Optional[str]
