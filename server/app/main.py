from fastapi import FastAPI
from app.routers import router_stock, router_user, router_watchlist, router_news, router_portfolio, router_account, router_transaction
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(router_stock.router)
app.include_router(router_user.router) 

app.include_router(router_watchlist.router)
app.include_router(router_news.router)
app.include_router(router_portfolio.router)
app.include_router(router_account.router)
app.include_router(router_transaction.router)


origins = [
    "http://localhost:8001", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)