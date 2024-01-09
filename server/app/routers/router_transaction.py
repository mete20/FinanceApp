from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_transaction
from app.schemas import schema_transaction
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[schema_transaction.Transaction])
def read_transactions(user_id: int, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    transactions = crud_transaction.get_transaction_history(db, user_id=user_id, skip=skip, limit=limit)
    return transactions

## TODO: Add a function to create a new transaction
@router.post("/", response_model=schema_transaction.Transaction)
def create_transaction(transaction: schema_transaction.TransactionCreate, db: Session = Depends(get_db)):
    # Creating a new entry
    new_transaction_entry = crud_transaction.create_transaction(db, transaction=transaction)
    return new_transaction_entry