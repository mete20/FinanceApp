from sqlalchemy.orm import Session
from app.models import model_watchlist, model_stock
from app.schemas import schema_watchlist

from sqlalchemy import func
from app.models import model_stock
from sqlalchemy.orm import Session
from app.models import model_watchlist, model_stock
from app.schemas import schema_watchlist
from sqlalchemy import func
from app.models import model_stock



def get_watchlist(db: Session, user_id: int):
    watchlist = db.query(model_watchlist.Watchlist)\
                  .filter(model_watchlist.Watchlist.userID == user_id)\
                  .all()

    return watchlist

def add_watchlist(db: Session, watchlist_data: schema_watchlist.WatchlistCreate):
    # Creating a new entry
    new_watchlist_entry = model_watchlist.Watchlist(**watchlist_data.dict())

    # if stock is already in watchlist, return None
    if isStockInWatchlist(db, watchlist_data):
        return None

    # Adding new entry to database
    db.add(new_watchlist_entry)
    db.commit()
    db.refresh(new_watchlist_entry)

    return new_watchlist_entry

def isStockInWatchlist(db: Session, watchlist_data: schema_watchlist.WatchlistCreate):
    # Get the user ID, stock ID, and quantity from watchlist_data
    user_id = watchlist_data.userID
    stock_id = watchlist_data.stockID

    # check if stock is already in watchlist
    watchlist = db.query(model_watchlist.Watchlist)\
                  .filter(model_watchlist.Watchlist.userID == user_id,
                          model_watchlist.Watchlist.stockID == stock_id)\
                  .first()

    return watchlist

def remove_stock_from_watchlist(db: Session, user_id: int, stock_id: int):

    watchlist = db.query(model_watchlist.Watchlist)\
      .filter(model_watchlist.Watchlist.userID == user_id,
              model_watchlist.Watchlist.stockID == stock_id)\
      .delete()
    db.commit()
    return watchlist

def get_watchlist_counts(db: Session, userID: int) -> int:
    count = db.query(func.count(model_watchlist.Watchlist.stockID))\
                .filter(model_watchlist.Watchlist.userID == userID)\
                .scalar()
    return int(count)


