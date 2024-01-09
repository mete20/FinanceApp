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