from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Portfolio(Base):
    __tablename__ = "portfolio"

    portfolioID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer)
    stockID = Column(Integer)
    quantity = Column(Integer)
    averagePrice = Column(Integer)

    



