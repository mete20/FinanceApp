from sqlalchemy.orm import Session
from app.models import model_stock
from app.schemas import schema_stock


def get_stocks(db: Session, skip: int = 0, limit: int = 200):
    return db.query(model_stock.Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: schema_stock.StockCreate):
    db_stock = model_stock.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock
