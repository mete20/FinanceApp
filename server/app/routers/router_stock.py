from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_stock
from app.schemas import schema_stock
from app.db.database import get_db
from typing import List

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
def create_movie(stock: schema_stock.StockCreate, db: Session = Depends(get_db)):
    return crud_stock.create_stock(db, stock)