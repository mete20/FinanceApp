from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    watchlistID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey('users.userID'))
    stockID = Column(Integer, ForeignKey('stocks.id'))

    #relationships
    stock = relationship("Stock", back_populates="watchlist_stock")
    user = relationship("User", back_populates="watchlist_user")

    

    



