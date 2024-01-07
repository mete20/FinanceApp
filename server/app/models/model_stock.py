from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True) 
    symbol = Column(String(255))
    current_price = Column(Float)



