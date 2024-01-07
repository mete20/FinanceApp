from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transactionID = Column(Integer, primary_key=True, index=True) 
    userID = Column(Integer)
    stockID = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
    timeStamp = Column(String(255))
    type = Column(String(255))



