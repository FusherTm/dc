"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.partners import router as partners_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router
from app.api.production import router as production_router
from app.api.financial import router as financial_router
from app.api.dashboard import router as dashboard_router

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(partners_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(production_router)
app.include_router(financial_router)
app.include_router(dashboard_router)
