from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_portfolio
from app.schemas import schema_portfolio
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[schema_portfolio.Portfolio])
def read_user_portfolio(user_id: int, db: Session = Depends(get_db)):
    portfolio = crud_portfolio.get_portfolio(db, user_id=user_id)
    return portfolio
