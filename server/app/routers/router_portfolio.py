from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_portfolio
from app.schemas import schema_portfolio
from app.db.database import get_db
from typing import List
from sqlalchemy import func
from app.crud.crud_portfolio import buy_stock_by_symbol, sell_stock_by_symbol

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[schema_portfolio.Portfolio])
def read_user_portfolio(user_id: int, db: Session = Depends(get_db)):
    portfolio = crud_portfolio.get_portfolio(db, user_id=user_id)
    return portfolio


@router.post("/", response_model=schema_portfolio.Portfolio)
def buy_stock(portfolio_data: schema_portfolio.PortfolioCreate, db: Session = Depends(get_db)):
    new_portfolio_entry = crud_portfolio.create_portfolio(db, portfolio_data=portfolio_data)
    if new_portfolio_entry:
        return new_portfolio_entry
    else:
        raise HTTPException(status_code=400, detail="Not enough money to buy stock")


@router.get("/total_value/{user_id}", response_model=float)
def get_total_portfolio_value(user_id: int, db: Session = Depends(get_db)):
    total_value = crud_portfolio.get_total_portfolio_value(db, user_id=user_id)
    return total_value or 0.0

@router.post("/sell_stock/", response_model=bool)
def sell_stock_endpoint(portfolio_data: schema_portfolio.PortfolioCreate, db: Session = Depends(get_db)):
    return crud_portfolio.sell_stock(db, portfolio_data=portfolio_data)

@router.get("/cash_vs_invested/{user_id}", response_model=dict)
def get_cash_vs_invested_value(user_id: int, db: Session = Depends(get_db)):
    return crud_portfolio.get_cash_vs_invested(db, user_id=user_id)


@router.post("/buy_stock_by_symbol/")
def buy_stock_by_symbol_endpoint(user_id: int, stock_symbol: str, quantity: int, db: Session = Depends(get_db)):
    success = buy_stock_by_symbol(db, user_id, stock_symbol, quantity)
    if success:
        return {"message": "Stock purchased successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not purchase stock")

@router.post("/sell_stock_by_symbol/")
def sell_stock_by_symbol_endpoint(user_id: int, stock_symbol: str, quantity: int, db: Session = Depends(get_db)):
    success = sell_stock_by_symbol(db, user_id, stock_symbol, quantity)
    if success:
        return {"message": "Stock sold successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not sell stock")