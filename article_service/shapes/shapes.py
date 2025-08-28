from pydantic import BaseModel

class Article(BaseModel):
    id : str
    title: str
    subtitle: str
    content: str
    tags: list[str]
