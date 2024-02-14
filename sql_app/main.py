from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

@dataclass
class Article(BaseModel):
    title: str
    content: str
    creation_date: str

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=list[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles

@app.get("/article/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_article

@app.post("/article/post", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db=db, article=article)

@app.put("/article/put/{article_id}")
def update_article(article_id: int, title: str, content: str, creation_date: str, db: Session = Depends(get_db)):
    crud.update_article(db, article_id=article_id, title=title, content=content, creation_date=creation_date)

@app.delete("/article/delete/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    crud.delete_article(db, article_id=article_id)