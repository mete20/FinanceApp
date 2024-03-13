from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base
from sqlalchemy.orm import relationship

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True) 
    symbol = Column(String(255))
    current_price = Column(Float)

    #relationships
    portfolio_stock = relationship("Portfolio", back_populates="stock")
    transaction_stock = relationship("Transaction", back_populates="stock")
    watchlist_stock = relationship("Watchlist", back_populates="stock")
    news_stock = relationship("News", back_populates="stock")




