from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    watchlistID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer)
    stockID = Column(Integer)



