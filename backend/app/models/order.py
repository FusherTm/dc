"""Order model."""

import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=False)
    status = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, server_default="0")
    tax_amount = Column(Numeric(10, 2), nullable=False, server_default="0")
    grand_total = Column(Numeric(10, 2), nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('TEKLIF','SIPARIS','URETIMDE')", name="ck_orders_status"),
    )

