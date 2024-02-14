from sqlalchemy import Column, Integer, String
from datetime import date

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    creation_date = Column(String)