from sqlalchemy.orm import Session
from app.models import model_stock, StockPriceHistory
from sqlalchemy import desc, func
from app.schemas import schema_stock
from datetime import datetime, timedelta

def get_stocks(db: Session, skip: int = 0, limit: int = 200):
    return db.query(model_stock.Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: schema_stock.StockCreate):
    db_stock = model_stock.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


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

