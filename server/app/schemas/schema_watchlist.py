from pydantic import BaseModel

class WatchlistBase(BaseModel):
    userID: int
    stockID: int

class WatchlistCreate(WatchlistBase):
    pass

class Watchlist(BaseModel):
    watchlistID: int
    class Config:
        orm_mode = True
