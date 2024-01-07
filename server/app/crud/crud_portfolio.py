from sqlalchemy.orm import Session
from app.models import model_portfolio


def get_portfolio(db: Session, user_id: int):
    return db.query(model_portfolio.Portfolio)\
             .filter(model_portfolio.Portfolio.userID == user_id)\
             .all()  
             
             
       

