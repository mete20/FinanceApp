from pydantic import BaseModel

class TransactionBase(BaseModel):
    userID: int
    stockID: int
    quantity: int
    price: float
    timeStamp: str
    type: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transactionID: int
    class Config:
        orm_mode = True
