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

import yfinance as yf
import pandas as pd


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


def updateAllStocks(db: Session):
    stocks = db.query(model_stock.Stock).all()
    for stock in stocks:
        stock.update_stock(db)
    db.commit()
    db.refresh(stock)
    return stock


def updateAllStocks(db: Session):
    stocks = db.query(model_stock.Stock).all()
    for stock in stocks:
        # Perform the logic to update the current price of the stock
        # For example, you can fetch the latest price from an API
        updated_price = fetch_latest_price(stock.symbol)
        
        if updated_price is None:
            # Skip this stock if no data was returned
            continue
        # Update the current price of the stock
        stock.current_price = updated_price
        
        # Commit the changes to the database
        db.commit()


def fetch_latest_price(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")
    if not hist.empty:
        # Get the latest closing price
        latest_price = hist['Close'].iloc[-1]
        return latest_price
    else:
        # Handle the case where no data was returned
        return None
    
def get_stock_by_symbol(db: Session, symbol: str):
        return db.query(model_stock.Stock).filter(model_stock.Stock.symbol == symbol).first()

def get_stocks_by_price_range(db: Session, min_price: float, max_price: float):
        return db.query(model_stock.Stock).filter(model_stock.Stock.current_price.between(min_price, max_price)).all()

def search_stocks_by_symbol_prefix(db: Session, prefix: str):
        return db.query(model_stock.Stock).filter(model_stock.Stock.symbol.like(f'{prefix}%')).all()



