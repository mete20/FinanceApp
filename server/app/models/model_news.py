from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class News(Base):
    __tablename__ = "news"

    newsID = Column(Integer, primary_key=True, index=True)
    stockID = Column(Integer)
    title = Column(String(255))
    content = Column(String(255))
    date = Column(String(255))


    



