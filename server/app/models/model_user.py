from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = "stocks"

    userID = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255))
    mail = Column(String(255))
    password = Column(String(255))
    accountID = Column(Integer) # accountID foreign key for account table



