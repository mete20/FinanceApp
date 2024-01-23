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

@router.get("/highest-price/")
def stocks_with_highest_price(limit: int = 10, db: Session = Depends(get_db)):
    return crud_stock.get_stocks_with_highest_price(db, limit)

@router.get("/lowest-price/")
def stocks_with_lowest_price(limit: int = 10, db: Session = Depends(get_db)):
    return crud_stock.get_stocks_with_lowest_price(db, limit)

@router.get("/update-all-stocks/", response_model= str)
def update_all_stocks(db: Session = Depends(get_db)):
    crud_stock.updateAllStocks(db)
    return "Stocks updated successfully"

@router.get("/{symbol}", response_model=schema_stock.Stock)
def get_stock_by_symbol(symbol: str, db: Session = Depends(get_db)):
    return crud_stock.get_stock_by_symbol(db, symbol)

@router.get("/price-range/{min_price}/{max_price}", response_model=List[schema_stock.Stock])
def get_stocks_by_price_range(min_price: float, max_price: float, db: Session = Depends(get_db)):
    return crud_stock.get_stocks_by_price_range(db, min_price, max_price)

@router.get("/search/{prefix}", response_model=List[schema_stock.Stock])
def search_stocks_by_symbol_prefix(prefix: str, db: Session = Depends(get_db)):
    return crud_stock.search_stocks_by_symbol_prefix(db, prefix)


