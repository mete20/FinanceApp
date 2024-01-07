from sqlalchemy.orm import Session
from app.models import model_transaction

def get_transaction_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model_transaction.Transaction)\
             .filter(model_transaction.Transaction.userID == user_id)\
             .offset(skip).limit(limit).all()
             
             

                    

