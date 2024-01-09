from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class News(Base):
    __tablename__ = "news"

    newsID = Column(Integer, primary_key=True, index=True)
    stockID = Column(Integer, ForeignKey('stocks.id'))
    title = Column(String(255))
    content = Column(String(255))
    date = Column(String(255))

    #relationships
    stock = relationship("Stock", back_populates="news_stock")


    



