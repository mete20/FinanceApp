from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_news
from app.schemas import schema_news
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schema_news.News])
def read_news(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    news = crud_news.get_news(db, skip=skip, limit=limit)
    return news

@router.get("/{stock_id}", response_model=schema_news.News)
def read_user_news(stock_id: int, db: Session = Depends(get_db)):
    news = crud_news.get_news_by_stock_id(db, stock_id=stock_id)
    return news

@router.post("/", response_model=schema_news.News)
def add_news_by_stock_id(news_data: schema_news.NewsCreate, db: Session = Depends(get_db)):
    new_news_entry = crud_news.add_news_by_stock_id(db, news_data=news_data)
    return new_news_entry

