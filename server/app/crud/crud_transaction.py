from sqlalchemy.orm import Session
from app.models import model_transaction
from app.schemas import schema_transaction

def get_transaction_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model_transaction.Transaction)\
             .filter(model_transaction.Transaction.userID == user_id)\
             .offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schema_transaction.TransactionCreate):
    db_transaction = model_transaction.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_buy_transaction_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model_transaction.Transaction)\
             .filter(model_transaction.Transaction.userID == user_id)\
             .filter(model_transaction.Transaction.type == "buy")\
             .offset(skip).limit(limit).all()

def get_sell_transaction_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model_transaction.Transaction)\
             .filter(model_transaction.Transaction.userID == user_id)\
             .filter(model_transaction.Transaction.type == "sell")\
             .offset(skip).limit(limit).all()

