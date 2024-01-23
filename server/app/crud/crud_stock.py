from datetime import timedelta
from sqlalchemy.orm import Session
from app.models import model_stock
from app.schemas import schema_stock
from sqlalchemy import func

from app.models.model_stock import Stock
from app.models.model_transaction import Transaction  
from app.models.model_news import News  
from app.models.model_portfolio import Portfolio  
from sqlalchemy import and_  
from app.models.model_watchlist import Watchlist  

def get_stocks(db: Session, skip: int = 0, limit: int = 200):
    return db.query(model_stock.Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: schema_stock.StockCreate):
    db_stock = model_stock.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_top_performing_stocks(db: Session, days_back: int = 30, top_n: int = 10):
    """
    Retrieves the top N performing stocks based on the percentage increase in price
    over the past specified number of days.
    """
    current_date = func.now()
    past_date = current_date - timedelta(days=days_back)

    subquery = db.query(
        model_stock.Stock.id,
        ((model_stock.Stock.current_price - model_stock.Stock.historical_price) / model_stock.Stock.historical_price).label('performance')
    ).filter(model_stock.Stock.date.between(past_date, current_date)).subquery()

    return db.query(model_stock.Stock).join(
        subquery, model_stock.Stock.id == subquery.c.id
    ).order_by(subquery.c.performance.desc()).limit(top_n).all()

def get_total_transaction_value_by_stock(db: Session):
    """
    Calculate the total value of transactions for each stock.
    """
    return db.query(
        Stock.symbol,
        (func.sum(Transaction.quantity * Transaction.price)).label('total_value')
    ).join(Stock.transaction_stock
    ).group_by(Stock.symbol
    ).all()

def get_latest_news_for_portfolio_stocks(db: Session, portfolio_id: int):
    
    """
    Get the latest piece of news for each stock in a given portfolio.
    """
    subquery = db.query(
        News.stock_id,
        func.max(News.date).label('latest_news_date')
    ).join(News.stock_news
    ).filter(Portfolio.id == portfolio_id
    ).group_by(News.stock_id
    ).subquery()

    return db.query(
        Stock.symbol, News.title, News.content
    ).join(Stock.news_stock
    ).join(subquery, and_(News.stock_id == subquery.c.stock_id, News.date == subquery.c.latest_news_date)
    ).all()



def get_average_price_of_watchlisted_stocks(db: Session, user_id: int):
    """
    Calculate the average current price of stocks in a specific user's watchlist.
    """
    return db.query(
        func.avg(Stock.current_price).label('average_price')
    ).join(Stock.watchlist_stock
    ).filter(Watchlist.user_id == user_id).scalar()

def get_stocks_with_highest_price(db: Session, limit: int = 10):
    return db.query(model_stock.Stock).order_by(model_stock.Stock.current_price.desc()).limit(limit).all()

def get_stocks_with_lowest_price(db: Session, limit: int = 10):
    return db.query(model_stock.Stock).order_by(model_stock.Stock.current_price.asc()).limit(limit).all()

