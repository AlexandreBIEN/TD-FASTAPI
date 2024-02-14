from pydantic import BaseModel
from datetime import date


class ArticleBase(BaseModel):
    title: str
    content: str
    creation_date: str


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int

    class Config:
        orm_mode = True