"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.partners import router as partners_router
from app.api.products import router as products_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(partners_router)
app.include_router(products_router)
