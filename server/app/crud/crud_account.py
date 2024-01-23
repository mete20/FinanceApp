from sqlalchemy.orm import Session
from app.models import model_account
from app.schemas import schema_account
from sqlalchemy.orm import Session
from app.models import model_account, model_user
from app.schemas import schema_account


def get_account(db: Session, user_id: int):
    return db.query(model_account.Account)\
             .filter(model_account.Account.userID == user_id)\
             .first() 

def get_accounts(db: Session):
    return db.query(model_account.Account).all()

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

def create_account_for_each_user(db: Session):
    # Get all users from the database
    users = db.query(model_user.User).all()

    # Create an account for each user
    for user in users:
        # Creating a new entry
        # if user has an account, skip
        if get_account(db, user.userID):
            continue
        new_account_entry = model_account.Account(userID=user.userID)

        # Adding new entry to database
        db.add(new_account_entry)
        db.commit()
        db.refresh(new_account_entry)

    return "Accounts created for each user"




             

             
           
        
