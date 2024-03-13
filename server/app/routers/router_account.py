from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_account
from app.schemas import schema_account
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=schema_account.Account)
def read_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = crud_account.get_account(db, user_id=user_id)
    return accounts

@router.get("/", response_model=List[schema_account.Account])
def read_accounts(db: Session = Depends(get_db)):
    accounts = crud_account.get_accounts(db)
    return accounts

## TODO: Add a function to create a new account
@router.post("/", response_model=schema_account.Account)
def create_account(account_data: schema_account.AccountCreate, db: Session = Depends(get_db)):
    # Creating a new entry
    new_account_entry = crud_account.create_account(db, account_data=account_data)
    return new_account_entry

@router.put("/{user_id}/add-money", response_model=schema_account.Account)
def add_money_to_balance(user_id: int, amount: float, db: Session = Depends(get_db)):
    account = crud_account.add_money_to_balance(db, user_id=user_id, amount=amount)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/create-account-for-each-user", response_model=str)
def create_account_for_each_user(db: Session = Depends(get_db)):
    return crud_account.create_account_for_each_user(db)
