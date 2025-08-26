from decimal import Decimal
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


# Account schemas
class AccountCreate(BaseModel):
    name: str


class AccountUpdate(BaseModel):
    name: str | None = None


class AccountPublic(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    current_balance: Decimal

    class Config:
        orm_mode = True


# Financial transaction schemas
TransactionDirection = Literal["IN", "OUT"]


class FinancialTransactionCreate(BaseModel):
    account_id: UUID
    partner_id: UUID | None = None
    order_id: UUID | None = None
    purchase_order_id: UUID | None = None
    direction: TransactionDirection
    amount: Decimal
    description: str | None = None


class FinancialTransactionUpdate(BaseModel):
    partner_id: UUID | None = None
    order_id: UUID | None = None
    purchase_order_id: UUID | None = None
    direction: TransactionDirection | None = None
    amount: Decimal | None = None
    description: str | None = None


class FinancialTransactionPublic(BaseModel):
    id: UUID
    organization_id: UUID
    account_id: UUID
    partner_id: UUID | None
    order_id: UUID | None
    purchase_order_id: UUID | None
    direction: TransactionDirection
    amount: Decimal
    transaction_date: datetime
    description: str | None

    class Config:
        orm_mode = True
