from sqlalchemy.orm import Session
from app.models import model_watchlist
from app.schemas import schema_watchlist



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

