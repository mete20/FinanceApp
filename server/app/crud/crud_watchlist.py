from sqlalchemy.orm import Session
from app.models import model_watchlist
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

    # Adding new entry to database
    db.add(new_watchlist_entry)
    db.commit()
    db.refresh(new_watchlist_entry)

    return new_watchlist_entry

def remove_stock_from_watchlist(db: Session, user_id: int, stock_id: int):
    """
    Remove a stock from a user's watchlist.
    """
    db.query(model_watchlist.Watchlist)\
      .filter(model_watchlist.Watchlist.userID == user_id,
              model_watchlist.Watchlist.stockID == stock_id)\
      .delete()
    db.commit()


def get_watchlist_summary(db: Session, user_id: int):
    """
    Get a summary of a user's watchlist, including the number of stocks and the average price.
    """
    return db.query(
        func.count(model_stock.Stock.id).label('number_of_stocks'),
        func.avg(model_stock.Stock.current_price).label('average_price')
    ).join(model_watchlist.Watchlist, model_watchlist.Watchlist.stockID == model_stock.Stock.id)\
     .filter(model_watchlist.Watchlist.userID == user_id)\
     .group_by(model_watchlist.Watchlist.userID)\
     .one_or_none()

def get_common_stocks_in_watchlists(db: Session, min_users: int = 2):
    """
    Find stocks that are common in the watchlists of at least min_users.
    """
    return db.query(
        model_stock.Stock.id,
        model_stock.Stock.symbol,
        func.count(model_watchlist.Watchlist.userID).label('user_count')
    ).join(model_watchlist.Watchlist, model_watchlist.Watchlist.stockID == model_stock.Stock.id)\
     .group_by(model_stock.Stock.id)\
     .having(func.count(model_watchlist.Watchlist.userID) >= min_users)\
     .all()