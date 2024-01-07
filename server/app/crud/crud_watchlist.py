from sqlalchemy.orm import Session
from app.models import model_watchlist



def get_watchlist(db: Session, user_id: int):
    watchlist = db.query(model_watchlist.Watchlist)\
                  .filter(model_watchlist.Watchlist.userID == user_id)\
                  .all()

    return watchlist

