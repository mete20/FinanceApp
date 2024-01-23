from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas import schema_user
from app.db.database import get_db
from typing import List
from app.models import model_transaction
from sqlalchemy import func
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schema_user.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schema_user.User)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user) 
