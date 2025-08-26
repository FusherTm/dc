"""Order CRUD endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.order import OrderCreate, OrderUpdate, OrderPublic, OrderStatus
from app.services.order_service import (
    create_order,
    get_order,
    get_orders,
    update_order,
    delete_order,
)

router = APIRouter(prefix="/api/orders", tags=["orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=OrderPublic)
def create_order_endpoint(order_in: OrderCreate, db: Session = Depends(get_db)) -> OrderPublic:
    try:
        return create_order(db, order_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/", response_model=List[OrderPublic])
def list_orders(
    page: int = 1,
    page_size: int = 10,
    partner_id: UUID | None = None,
    status: OrderStatus | None = None,
    db: Session = Depends(get_db),
) -> List[OrderPublic]:
    return get_orders(db, page, page_size, partner_id, status)


@router.get("/{order_id}", response_model=OrderPublic)
def read_order(order_id: UUID, db: Session = Depends(get_db)) -> OrderPublic:
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderPublic)
def update_order_endpoint(
    order_id: UUID, order_in: OrderUpdate, db: Session = Depends(get_db)
) -> OrderPublic:
    try:
        order = update_order(db, order_id, order_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_endpoint(order_id: UUID, db: Session = Depends(get_db)) -> None:
    success = delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return None
