from pydantic import BaseModel

class Article(BaseModel):
    title: str
    subtitle: str
    content: str
    tags: list[str]
