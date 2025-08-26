from decimal import Decimal
from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel

from .order_item import OrderItemCreate, OrderItemUpdate, OrderItemPublic

OrderStatus = Literal["TEKLIF", "SIPARIS", "URETIMDE", "TESLIM EDILDI"]


class OrderCreate(BaseModel):
    partner_id: UUID
    status: OrderStatus
    order_items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    partner_id: UUID | None = None
    status: OrderStatus | None = None
    order_items: List[OrderItemUpdate] | None = None


class OrderPublic(BaseModel):
    id: UUID
    organization_id: UUID
    partner_id: UUID
    status: OrderStatus
    total_amount: Decimal
    tax_amount: Decimal
    grand_total: Decimal
    order_items: List[OrderItemPublic]

    class Config:
        orm_mode = True
