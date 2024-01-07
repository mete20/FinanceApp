from sqlalchemy.orm import Session


"""
def get_transaction_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model_transaction.TransactionHistory)\
             .filter(model_transaction.TransactionHistory.user_id == user_id)\
             .offset(skip).limit(limit).all()
             
             

                    
             
"""
