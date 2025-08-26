from datetime import datetime
from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel

JobStatus = Literal["PENDING", "IN_PROGRESS", "COMPLETED"]


class ProductionLogCreate(BaseModel):
    station_id: UUID
    user_id: UUID
    quantity: int


class ProductionLogPublic(BaseModel):
    id: UUID
    job_id: UUID
    station_id: UUID
    user_id: UUID
    completed_at: datetime
    quantity: int

    class Config:
        orm_mode = True


class ProductionJobCreate(BaseModel):
    order_item_id: UUID
    quantity_required: int


class ProductionJobUpdate(BaseModel):
    status: JobStatus | None = None
    quantity_produced: int | None = None


class ProductionJobPublic(BaseModel):
    id: UUID
    organization_id: UUID
    order_item_id: UUID
    quantity_required: int
    quantity_produced: int
    status: JobStatus
    logs: List[ProductionLogPublic]

    class Config:
        orm_mode = True
