from datetime import timedelta
from sqlalchemy.orm import Session

from app.models import model_stock, model_stock_price_history
from app.schemas import schema_stock, schema_stock_price_history
from sqlalchemy import func, desc

from app.models.model_stock import Stock
from app.models.model_transaction import Transaction  
from app.models.model_news import News  
from app.models.model_portfolio import Portfolio  
from sqlalchemy import and_  
from app.models.model_watchlist import Watchlist 
from datetime import datetime, timedelta

def get_stocks(db: Session, skip: int = 0, limit: int = 200):
    return db.query(model_stock.Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: schema_stock.StockCreate):
    db_stock = model_stock.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

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

def get_top_performing_stocks(db: Session, days: int = 30, top_n: int = 10):


    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Subquery to get the earliest price in the specified time frame for each stock
    earliest_prices = (
        db.query(
            StockPriceHistory.stockID,
            func.min(StockPriceHistory.date).label('min_date')
        )
        .filter(StockPriceHistory.date >= start_date)
        .group_by(StockPriceHistory.stockID)
        .subquery()
    )

    # Subquery to get the latest price in the specified time frame for each stock
    latest_prices = (
        db.query(
            StockPriceHistory.stockID,
            func.max(StockPriceHistory.date).label('max_date')
        )
        .filter(StockPriceHistory.date <= end_date)
        .group_by(StockPriceHistory.stockID)
        .subquery()
    )

    # Main query to calculate the percentage increase for each stock
    top_stocks_query = (
        db.query(
            model_stock.Stock,
            ((StockPriceHistory.price / earliest_prices.c.price) - 1).label('percentage_increase')
        )
        .join(StockPriceHistory, model_stock.Stock.id == StockPriceHistory.stockID)
        .join(earliest_prices, and_(model_stock.Stock.id == earliest_prices.c.stockID, StockPriceHistory.date == earliest_prices.c.min_date))
        .join(latest_prices, and_(model_stock.Stock.id == latest_prices.c.stockID, StockPriceHistory.date == latest_prices.c.max_date))
        .order_by(desc('percentage_increase'))
        .limit(top_n)
        .all()
    )

    return top_stocks_query

