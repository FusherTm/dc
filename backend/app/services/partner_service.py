"""Service layer for partner operations."""

import uuid
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.schemas.partner import PartnerCreate, PartnerUpdate

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def create_partner(db: Session, partner_in: PartnerCreate) -> Partner:
    partner = Partner(
        organization_id=DEFAULT_ORGANIZATION_ID,
        type=partner_in.type,
        name=partner_in.name,
        email=partner_in.email,
    )
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner


def get_partner(db: Session, partner_id: UUID) -> Optional[Partner]:
    return db.query(Partner).filter(Partner.id == partner_id).first()


def get_partners(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search_query: str | None = None,
) -> List[Partner]:
    query = db.query(Partner)
    if search_query:
        query = query.filter(Partner.name.ilike(f"%{search_query}%"))
    return query.offset((page - 1) * page_size).limit(page_size).all()


def update_partner(
    db: Session, partner_id: UUID, partner_in: PartnerUpdate
) -> Optional[Partner]:
    partner = get_partner(db, partner_id)
    if not partner:
        return None
    for field, value in partner_in.dict(exclude_unset=True).items():
        setattr(partner, field, value)
    db.commit()
    db.refresh(partner)
    return partner


def delete_partner(db: Session, partner_id: UUID) -> bool:
    partner = get_partner(db, partner_id)
    if not partner:
        return False
    db.delete(partner)
    db.commit()
    return True
