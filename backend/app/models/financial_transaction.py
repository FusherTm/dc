"""Financial transaction model."""

import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"))
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    purchase_order_id = Column(UUID(as_uuid=True), ForeignKey("purchase_orders.id"))
    direction = Column(String(10), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("direction IN ('IN','OUT')", name="ck_financial_transactions_direction"),
    )

