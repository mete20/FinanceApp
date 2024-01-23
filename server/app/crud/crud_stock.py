from datetime import timedelta
from sqlalchemy.orm import Session

from app.models import model_stock #, model_stock_price_history
from app.schemas import schema_stock #, schema_stock_price_history
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

def get_stocks_with_highest_price(db: Session, limit: int = 10):
    return db.query(model_stock.Stock).order_by(model_stock.Stock.current_price.desc()).limit(limit).all()

def get_stocks_with_lowest_price(db: Session, limit: int = 10):
    return db.query(model_stock.Stock).order_by(model_stock.Stock.current_price.asc()).limit(limit).all()
