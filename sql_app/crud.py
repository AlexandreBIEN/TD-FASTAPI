from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas


def get_article_by_id(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: int, title: str, content: str, creation_date: str):
    db_article = get_article_by_id(db, article_id)
    
    if db_article:
        db_article.title = title
        db_article.content = content
        db_article.creation_date = creation_date
        db.commit()
        db.refresh(db_article)
    else :
        raise HTTPException(status_code=404, detail="L'article n'a pas été trouvé")
    return ""

def delete_article(db: Session, article_id: int):
    db_article = get_article_by_id(db, article_id)
    db.delete(db_article)
    db.commit()
    db.refresh(db_article)
    return ""