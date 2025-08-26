"""Partner CRUD endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.partner import PartnerCreate, PartnerUpdate, PartnerPublic
from app.services.partner_service import (
    create_partner,
    get_partner,
    get_partners,
    update_partner,
    delete_partner,
)

router = APIRouter(prefix="/api/partners", tags=["partners"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PartnerPublic)
def create_partner_endpoint(
    partner_in: PartnerCreate, db: Session = Depends(get_db)
) -> PartnerPublic:
    return create_partner(db, partner_in)


@router.get("/{partner_id}", response_model=PartnerPublic)
def read_partner(partner_id: UUID, db: Session = Depends(get_db)) -> PartnerPublic:
    partner = get_partner(db, partner_id)
    if not partner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")
    return partner


@router.get("/", response_model=List[PartnerPublic])
def list_partners(
    page: int = 1,
    page_size: int = 10,
    search_query: str | None = None,
    db: Session = Depends(get_db),
) -> List[PartnerPublic]:
    return get_partners(db, page, page_size, search_query)


@router.put("/{partner_id}", response_model=PartnerPublic)
def update_partner_endpoint(
    partner_id: UUID, partner_in: PartnerUpdate, db: Session = Depends(get_db)
) -> PartnerPublic:
    partner = update_partner(db, partner_id, partner_in)
    if not partner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")
    return partner


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner_endpoint(partner_id: UUID, db: Session = Depends(get_db)) -> None:
    success = delete_partner(db, partner_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")
    return None
