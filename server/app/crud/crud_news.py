from sqlalchemy.orm import Session
from app.models import model_news
from app.schemas import schema_news


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



