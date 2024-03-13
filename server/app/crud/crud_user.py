from sqlalchemy.orm import Session
from app.models import model_user, model_transaction
from app.schemas import schema_user, schema_account
from app.crud import crud_account, crud_watchlist, crud_portfolio
from sqlalchemy import func

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_user.User).offset(skip).limit(limit).all()
    
def create_user(db: Session, user: schema_user.UserCreate):
    db_user = model_user.User(**user.dict())  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create an empty account for the user
    crud_account.create_account(db, schema_account.AccountCreate(userID=db_user.userID, balance=0, balance_USD=0))
    
    return db_user   
   

