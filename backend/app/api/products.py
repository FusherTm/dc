"""Product CRUD endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate, ProductPublic
from app.services.product_service import (
    create_product,
    get_product,
    get_products,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/api/products", tags=["products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProductPublic)
def create_product_endpoint(
    product_in: ProductCreate, db: Session = Depends(get_db)
) -> ProductPublic:
    return create_product(db, product_in)


@router.get("/{product_id}", response_model=ProductPublic)
def read_product(product_id: UUID, db: Session = Depends(get_db)) -> ProductPublic:
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get("/", response_model=List[ProductPublic])
def list_products(
    page: int = 1,
    page_size: int = 10,
    search_query: str | None = None,
    db: Session = Depends(get_db),
) -> List[ProductPublic]:
    return get_products(db, page, page_size, search_query)


@router.put("/{product_id}", response_model=ProductPublic)
def update_product_endpoint(
    product_id: UUID, product_in: ProductUpdate, db: Session = Depends(get_db)
) -> ProductPublic:
    product = update_product(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: UUID, db: Session = Depends(get_db)) -> None:
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None
