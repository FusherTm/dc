"""Purchase order model."""

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=False)
    grand_total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

