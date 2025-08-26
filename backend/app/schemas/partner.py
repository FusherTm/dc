from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr

PartnerType = Literal["CUSTOMER", "SUPPLIER", "BOTH"]


class PartnerCreate(BaseModel):
    type: PartnerType
    name: str
    email: EmailStr | None = None


class PartnerUpdate(BaseModel):
    type: PartnerType | None = None
    name: str | None = None
    email: EmailStr | None = None


class PartnerPublic(BaseModel):
    id: UUID
    organization_id: UUID
    type: PartnerType
    name: str
    email: EmailStr | None = None

    class Config:
        orm_mode = True
