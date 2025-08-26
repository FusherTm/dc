"""Service layer for product operations."""

import uuid
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(
        organization_id=DEFAULT_ORGANIZATION_ID,
        name=product_in.name,
        base_price_sqm=product_in.base_price_sqm,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: UUID) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search_query: str | None = None,
) -> List[Product]:
    query = db.query(Product)
    if search_query:
        query = query.filter(Product.name.ilike(f"%{search_query}%"))
    return query.offset((page - 1) * page_size).limit(page_size).all()


def update_product(
    db: Session, product_id: UUID, product_in: ProductUpdate
) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None
    for field, value in product_in.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: UUID) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
