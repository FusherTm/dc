"""Partner model for customers and suppliers."""

import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('CUSTOMER','SUPPLIER','BOTH')", name="ck_partners_type"),
    )

