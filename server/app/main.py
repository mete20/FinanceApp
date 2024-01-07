from fastapi import FastAPI
from app.routers import router_stock
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router_stock.router)

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