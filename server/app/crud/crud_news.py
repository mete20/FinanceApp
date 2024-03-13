from sys import prefix
from sqlalchemy.orm import Session
from app.models import model_news
from app.schemas import schema_news
from app.models import model_stock
from app.crud import crud_stock
from sqlalchemy import func


def get_news(db: Session, skip: int = 0, limit: int = 100):
    news_entries = db.query(model_news.News)\
                     .offset(skip)\
                     .limit(limit)\
                     .all()
    return news_entries


def get_news_by_stock_id(db: Session, stock_id: int, skip: int = 0, limit: int = 100):
    news_entries = db.query(model_news.News)\
                     .filter(model_news.News.stockID == stock_id)\
                     .offset(skip)\
                     .limit(limit)\
                     .all()
    return news_entries


def add_news_by_stock_id(db: Session, news_data: schema_news.NewsCreate):
    # Creating a new entry
    new_news_entry = model_news.News(**news_data.dict())

    # Adding new entry to database
    db.add(new_news_entry)
    db.commit()
    db.refresh(new_news_entry)

    return new_news_entry


def get_news_by_stock_symbol_prefix(db: Session, symbol: str, skip: int = 0, limit: int = 100):
    stocks = crud_stock.search_stocks_by_symbol_prefix(db, symbol)
    news_entries = []
    for stock in stocks:
        news_entries += db.query(model_news.News)\
                          .filter(model_news.News.stockID == stock.id)\
                          .offset(skip)\
                          .limit(limit)\
                          .all()
    return news_entries

    
def get_news_by_stock_symbol(db: Session, symbol: str, skip: int = 0, limit: int = 100):
    stock = db.query(model_stock.Stock).filter(model_stock.Stock.symbol == symbol).first()
    
    if stock:
        news_entries = db.query(model_news.News)\
                        .filter(model_news.News.stockID == stock.id)\
                        .offset(skip)\
                        .limit(limit)\
                        .all()
        return news_entries
    else:
        return []

def count_news_by_stock_id(db: Session, stock_id: int):
    count = db.query(func.count(model_news.News.stockID))\
              .filter(model_news.News.stockID == stock_id)\
              .scalar()
    return count

def search_news_by_title(db: Session, title_pattern: str):
    like_pattern = f"%{title_pattern}%"
    return db.query(model_news.News)\
             .filter(model_news.News.title.like(like_pattern))\
             .all()

