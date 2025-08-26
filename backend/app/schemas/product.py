from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    base_price_sqm: Decimal


class ProductUpdate(BaseModel):
    name: str | None = None
    base_price_sqm: Decimal | None = None


class ProductPublic(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    base_price_sqm: Decimal

    class Config:
        orm_mode = True
