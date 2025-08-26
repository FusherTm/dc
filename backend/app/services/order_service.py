"""Service layer for order operations."""

import uuid
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TAX_RATE = Decimal("0.18")


def _create_order_item(db: Session, order_id: UUID, item_in) -> Decimal:
    """Helper to create an order item and return its total price."""
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise ValueError("Product not found")
    unit_price = product.base_price_sqm
    area_sqm = (Decimal(item_in.width) * Decimal(item_in.height)) / Decimal(1_000_000)
    total_price = unit_price * area_sqm * item_in.quantity
    order_item = OrderItem(
        organization_id=DEFAULT_ORGANIZATION_ID,
        order_id=order_id,
        product_id=item_in.product_id,
        width=item_in.width,
        height=item_in.height,
        quantity=item_in.quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
    db.add(order_item)
    return total_price


def create_order(db: Session, order_in: OrderCreate) -> Order:
    order = Order(
        organization_id=DEFAULT_ORGANIZATION_ID,
        partner_id=order_in.partner_id,
        status=order_in.status,
    )
    db.add(order)
    db.flush()
    total_amount = Decimal("0")
    for item in order_in.order_items:
        total_amount += _create_order_item(db, order.id, item)
    order.total_amount = total_amount
    order.tax_amount = total_amount * TAX_RATE
    order.grand_total = order.total_amount + order.tax_amount
    db.commit()
    db.refresh(order)
    order.order_items = (
        db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    )
    return order


def get_order(db: Session, order_id: UUID) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return order


def get_orders(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    partner_id: UUID | None = None,
    status: str | None = None,
) -> List[Order]:
    query = db.query(Order)
    if partner_id:
        query = query.filter(Order.partner_id == partner_id)
    if status:
        query = query.filter(Order.status == status)
    orders = query.offset((page - 1) * page_size).limit(page_size).all()
    for order in orders:
        order.order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return orders


def update_order(db: Session, order_id: UUID, order_in: OrderUpdate) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    for field in ["partner_id", "status"]:
        value = getattr(order_in, field)
        if value is not None:
            setattr(order, field, value)
    if order_in.order_items is not None:
        db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
        db.flush()
        total_amount = Decimal("0")
        for item in order_in.order_items:
            total_amount += _create_order_item(db, order.id, item)
        order.total_amount = total_amount
        order.tax_amount = total_amount * TAX_RATE
        order.grand_total = order.total_amount + order.tax_amount
    db.commit()
    db.refresh(order)
    order.order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return order


def delete_order(db: Session, order_id: UUID) -> bool:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True
