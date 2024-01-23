from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    accountID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey('users.userID'))
    balance = Column(Float, default=0.0)
    balance_USD = Column(Float, default=0.0)
    current_stock_value = Column(Float, default=0.0)

    #relationships
    user = relationship("User", back_populates="account")
    


    



