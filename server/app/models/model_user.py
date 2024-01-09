from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255))
    mail = Column(String(255))
    password = Column(String(255))
    
    #relationships
    account = relationship("Account", back_populates="user")
    portfolio_user = relationship("Portfolio", back_populates="user")
    watchlist_user = relationship("Watchlist", back_populates="user")
    transaction_user = relationship("Transaction", back_populates="user")
    



