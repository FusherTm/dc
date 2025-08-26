"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.partners import router as partners_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router
from app.api.production import router as production_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(partners_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(production_router)
