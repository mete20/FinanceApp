from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_stock
from app.schemas import schema_stock
from app.db.database import get_db
from typing import List
from fastapi import HTTPException

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schema_stock.Stock])
def read_stocks(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    stocks = crud_stock.get_stocks(db, skip=skip, limit=limit)
    return stocks

@router.post("/", response_model=schema_stock.Stock)
def create_stock(stock: schema_stock.StockCreate, db: Session = Depends(get_db)):
    return crud_stock.create_stock(db, stock)

@router.get("/top-performing/")
def get_top_performing_stocks(days_back: int = 30, top_n: int = 10, db: Session = Depends(get_db)):
    return crud_stock.get_top_performing_stocks(db, days_back, top_n)

@router.get("/transaction-total/")
def total_transaction_value_by_stock(db: Session = Depends(get_db)):
    return crud_stock.get_total_transaction_value_by_stock(db)

@router.get("/latest-news/")
def latest_news_for_portfolio_stocks(portfolio_id: int, db: Session = Depends(get_db)):
    return crud_stock.get_latest_news_for_portfolio_stocks(db, portfolio_id)

@router.get("/watchlist/average-price/")
def average_price_of_watchlisted_stocks(user_id: int, db: Session = Depends(get_db)):
    return crud_stock.get_average_price_of_watchlisted_stocks(db, user_id)

@router.get("/highest-price/")
def stocks_with_highest_price(limit: int = 10, db: Session = Depends(get_db)):
    return crud_stock.get_stocks_with_highest_price(db, limit)

@router.get("/lowest-price/")
def stocks_with_lowest_price(limit: int = 10, db: Session = Depends(get_db)):
    return crud_stock.get_stocks_with_lowest_price(db, limit)


