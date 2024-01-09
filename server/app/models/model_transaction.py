from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transactionID = Column(Integer, primary_key=True, index=True) 
    userID = Column(Integer, ForeignKey('users.userID'))
    stockID = Column(Integer, ForeignKey('stocks.id'))
    quantity = Column(Integer)
    price = Column(Integer)
    timeStamp = Column(String(255))
    type = Column(String(255))

    #relationships
    stock = relationship("Stock", back_populates="transaction_stock")
    user = relationship("User", back_populates="transaction_user")



