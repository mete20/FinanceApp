from sqlalchemy.orm import Session
from app.models import model_account


def get_account(db: Session, user_id: int):
    return db.query(model_account.Account)\
             .filter(model_account.Account.userID == user_id)\
             .first() 
             
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

def convert_balance_to_usd(db: Session, user_id: int):
    # Finding account of user
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()

    if not account:
        return "Account not found"

    # Setting exchange rate
    exchange_rate = 30  # 1 USD = 30 TL

    # Converting balance from TL to USD and update balance_usd
    account.balance_USD = account.balance / exchange_rate

    # Commit the changes to the database
    db.commit()

    return account    


def convert_balance_to_tl(db: Session, user_id: int):
    # Finding account of user
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()

    if not account:
        return "Account not found"

    # Setting exchange rate
    exchange_rate = 30  # 1 USD = 30 TL

    # Converting balance from USD to TL and update balance
    account.balance = account.balance_USD * exchange_rate

    # Committing changes to database
    db.commit()

    return account             
             
def add_money_to_balance_usd(db: Session, user_id: int, amount_usd: float):
    # Finding account of user
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()

    if not account:
        return "Account not found"

    # Adding amount in USD to account balance (USD)
    account.balance_USD += amount_usd

    # Committing changes to database
    db.commit()

    return account         
             

             
           
        
