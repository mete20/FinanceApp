from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_portfolio
from app.schemas import schema_portfolio
from app.db.database import get_db
from typing import List
from sqlalchemy import func

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[schema_portfolio.Portfolio])
def read_user_portfolio(user_id: int, db: Session = Depends(get_db)):
    portfolio = crud_portfolio.get_portfolio(db, user_id=user_id)
    return portfolio


@router.post("/", response_model=List[schema_portfolio.Portfolio])
def buy_stock(portfolio_data: schema_portfolio.PortfolioCreate, db: Session = Depends(get_db)):
    new_portfolio_entry = crud_portfolio.create_portfolio(db, portfolio_data=portfolio_data)
    return new_portfolio_entry


@router.get("/total_value/{user_id}", response_model=float)
def get_total_portfolio_value(user_id: int, db: Session = Depends(get_db)):
    total_value = crud_portfolio.get_total_portfolio_value(db, user_id=user_id)
    return total_value or 0.0

