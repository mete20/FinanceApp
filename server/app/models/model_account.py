from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Account(Base):
    __tablename__ = "account"

    accountID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer)
    balance = Column(Float)
    balance_USD = Column(Float)
    current_stock_value = Column(Float)
    


    



