from pydantic import BaseModel

class PortfolioBase(BaseModel):
    userID: int
    stockID: int
    quantity: int
    averagePrice: float

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    portfolioID: int
    class Config:
        orm_mode = True
