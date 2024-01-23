from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_watchlist
from app.schemas import schema_watchlist
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/watchlist",
    tags=["watchlist"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[schema_watchlist.Watchlist])
def read_watchlist(user_id: int, db: Session = Depends(get_db)):
    watchlist = crud_watchlist.get_watchlist(db, user_id=user_id)
    return watchlist

@router.post("/", response_model=schema_watchlist.Watchlist)
def create_watchlist(watchlist_data: schema_watchlist.WatchlistCreate, db: Session = Depends(get_db)):
    # Creating a new entry
    new_watchlist_entry = crud_watchlist.add_watchlist(db, watchlist_data=watchlist_data)
    return new_watchlist_entry

@router.delete("/{user_id}/{stock_id}", response_model=bool)
def delete_stock_from_watchlist(user_id: int, stock_id: int, db: Session = Depends(get_db)):
    crud_watchlist.remove_stock_from_watchlist(db, user_id=user_id, stock_id=stock_id)
    return True

@router.get("/summary/{user_id}", response_model=dict)
def get_watchlist_summary(user_id: int, db: Session = Depends(get_db)):
    summary = crud_watchlist.get_watchlist_summary(db, user_id=user_id)
    return summary if summary else {"number_of_stocks": 0, "average_price": 0.0}

@router.get("/common-stocks/", response_model=List[schema_watchlist.CommonStocks])
def get_common_stocks(min_users: int = 2, db: Session = Depends(get_db)):
    return crud_watchlist.get_common_stocks_in_watchlists(db, min_users=min_users)