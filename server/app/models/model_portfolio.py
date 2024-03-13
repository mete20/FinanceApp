from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Portfolio(Base):
    __tablename__ = "portfolio"

    portfolioID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey('users.userID'))
    stockID = Column(Integer, ForeignKey('stocks.id'))
    quantity = Column(Integer)
    averagePrice = Column(Integer)

    #relationships
    stock = relationship("Stock", back_populates="portfolio_stock")
    user = relationship("User", back_populates="portfolio_user")

