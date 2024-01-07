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


@router.get("/{user_id}", response_model=List[schema_account.Account])
def read_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = crud_account.get_accounts(db, user_id=user_id)
    return accounts


@router.put("/{user_id}/add-money", response_model=schema_account.Account)
def add_money_to_balance(user_id: int, amount: float, db: Session = Depends(get_db)):
    account = crud_account.add_money_to_balance(db, user_id=user_id, amount=amount)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{user_id}/convert-balance-to-usd", response_model=schema_account.Account)
def convert_balance_to_usd(user_id: int, db: Session = Depends(get_db)):
    account = crud_account.convert_balance_to_usd(db, user_id=user_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{user_id}/convert-balance-to-tl", response_model=schema_account.Account)
def convert_balance_to_tl(user_id: int, db: Session = Depends(get_db)):
    account = crud_account.convert_balance_to_tl(db, user_id=user_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{user_id}/add-money-usd", response_model=schema_account.Account)
def add_money_to_balance_usd(user_id: int, amount_usd: float, db: Session = Depends(get_db)):
    account = crud_account.add_money_to_balance_usd(db, user_id=user_id, amount_usd=amount_usd)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
