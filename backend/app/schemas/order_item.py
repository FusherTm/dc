from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: UUID
    width: int
    height: int
    quantity: int


class OrderItemUpdate(BaseModel):
    product_id: UUID
    width: int
    height: int
    quantity: int


class OrderItemPublic(BaseModel):
    id: UUID
    product_id: UUID
    width: int
    height: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        orm_mode = True
