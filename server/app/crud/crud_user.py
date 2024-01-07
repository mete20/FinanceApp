from sqlalchemy.orm import Session
from app.models import model_user
from app.schemas import schema_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_user.User).offset(skip).limit(limit).all()
    
def create_user(db: Session, user: schema_user.UserCreate):
    db_user = model_user.User(**user.dict())  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user   
   

