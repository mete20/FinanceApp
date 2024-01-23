from sqlalchemy.orm import Session
from app.models import model_account
from app.schemas import schema_account


def get_account(db: Session, user_id: int):
    return db.query(model_account.Account)\
             .filter(model_account.Account.userID == user_id)\
             .first() 


def create_account(db: Session, account_data: schema_account.AccountCreate):
    # Creating a new entry
    new_account_entry = model_account.Account(**account_data.dict())

    # Adding new entry to database
    db.add(new_account_entry)
    db.commit()
    db.refresh(new_account_entry)

    return new_account_entry
             
def add_money_to_balance(db: Session, user_id: int, amount: float):
    # Finding account of user
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()

    if not account:
        return "Account not found"

    # Adding amount to account balance
    account.balance += amount

    # Committing changes to  db
    db.commit()

    return account




             

             
           
        
