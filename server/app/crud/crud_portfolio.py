from sqlalchemy.orm import Session
from app.models import model_portfolio, model_account, model_stock
from app.schemas import schema_portfolio
from sqlalchemy import func
from app.models import model_portfolio
from app.models import model_portfolio, model_stock



def get_portfolio(db: Session, user_id: int):
    return db.query(model_portfolio.Portfolio)\
             .filter(model_portfolio.Portfolio.userID == user_id)\
             .all()  


def create_portfolio(db: Session, portfolio_data: schema_portfolio.PortfolioCreate):
    # check user has enough money to buy the stock
    if user_has_enough_money(db, portfolio_data):
        # buy the stock
        return buy_stock(db, portfolio_data) 
    else:
        return "Error: Not enough money to buy the stock."


def user_has_enough_money(db: Session, portfolio_data):
    # implementation to check if user has enough money
    # return True if user has enough money, False otherwise
    balance = get_balance(db, portfolio_data)
    stock_price = get_stock_price(db, portfolio_data)
    if balance >= stock_price:
        return True
    else:
        return False


def buy_stock(db: Session, portfolio_data):
    # Get the user ID, stock ID, and quantity from portfolio_data
    user_id = portfolio_data.userID
    quantity = portfolio_data.quantity

    # Update the balance in the account table
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()
    if account:
        account.balance -= quantity * get_stock_price(db, portfolio_data)
        db.commit()

    # Add new entry to portfolio table
    new_portfolio_entry = model_portfolio.Portfolio(**portfolio_data.dict())
    db.add(new_portfolio_entry)
    db.commit()
    db.refresh(new_portfolio_entry)
    return new_portfolio_entry
             
def get_balance(db: Session, portfolio_data):
    # implementation to get balance
    # I have userId from portfolio_data, I need to get balance from account table
    user_id = portfolio_data.userID
    account = db.query(model_account.Account).filter(model_account.Account.userID == user_id).first()
    if account:
        return account.balance
    else:
        return 0
       
def get_stock_price(db: Session, portfolio_data):
    # implementation to get stock price
    stock_id = portfolio_data.stockID
    stock = db.query(model_stock.Stock).filter(model_stock.Stock.id == stock_id).first()
    if stock:
        return stock.current_price
    else:
        return 0
    
def get_total_portfolio_value(db: Session, user_id: int) -> float:
    total_value = db.query(func.sum(model_portfolio.Portfolio.quantity * model_stock.Stock.current_price)). \
        join(model_stock.Stock, model_portfolio.Portfolio.stockID == model_stock.Stock.id). \
        filter(model_portfolio.Portfolio.userID == user_id).scalar()
    return total_value or 0.0  # Return 0.0 if no portfolio data found

def get_cash_vs_invested(db: Session, user_id: int):
    """
    Compare the uninvested cash in the account with the invested amount.
    """
    invested_amount = get_total_portfolio_value(db, user_id)
    cash_balance = get_balance(db, user_id)
    return {'invested': invested_amount, 'cash_balance': cash_balance}

def sell_stock(db: Session, portfolio_data):
    # Get the user ID, stock ID, and quantity from portfolio_data
    user_id = portfolio_data.userID
    stock_id = portfolio_data.stockID
    quantity = portfolio_data.quantity
    
    # Check if the user owns the stock
    portfolio = db.query(model_portfolio.Portfolio).filter(
        model_portfolio.Portfolio.userID == user_id,
        model_portfolio.Portfolio.stockID == stock_id
    ).first()
    
    if portfolio:
        # Check if the user has enough quantity to sell
        if portfolio.quantity >= quantity:
            # Update the portfolio quantity
            portfolio.quantity -= quantity
            
            # Update the user's account balance
            stock_price = get_stock_price(db, portfolio_data)
            sale_amount = stock_price * quantity
            account = db.query(model_account.Account).filter(
                model_account.Account.userID == user_id
            ).first()
            
            if account:
                account.balance += sale_amount
            else:
                # Create a new account for the user if it doesn't exist
                account = model_account.Account(userID=user_id, balance=sale_amount)
                db.add(account)
            
            db.commit()
            return True
        else:
            return False  # User doesn't have enough quantity to sell
    else:
        return False  # User doesn't own the stock

