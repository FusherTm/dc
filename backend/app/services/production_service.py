"""Service layer for production operations."""

import uuid
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.models.production_job import ProductionJob
from app.models.production_log import ProductionLog
from app.models.production_station import ProductionStation
from app.schemas.production import ProductionLogCreate

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
DEFAULT_STATIONS = [
    ("Cam Kesim", "CAM_KESIM", 1),
    ("Pres", "PRES", 2),
]


def _ensure_default_stations(db: Session) -> None:
    for name, code, order_index in DEFAULT_STATIONS:
        exists = db.query(ProductionStation).filter(ProductionStation.code == code).first()
        if not exists:
            station = ProductionStation(
                organization_id=DEFAULT_ORGANIZATION_ID,
                name=name,
                code=code,
                order_index=order_index,
            )
            db.add(station)
    db.flush()


def create_job_from_order_item(db: Session, order_item_id: UUID) -> ProductionJob:
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise ValueError("Order item not found")
    _ensure_default_stations(db)
    job = ProductionJob(
        organization_id=DEFAULT_ORGANIZATION_ID,
        order_item_id=order_item_id,
        quantity_required=order_item.quantity,
    )
    db.add(job)
    db.flush()
    return job


def get_jobs(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    status: str | None = None,
) -> List[ProductionJob]:
    query = db.query(ProductionJob)
    if status:
        query = query.filter(ProductionJob.status == status)
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()
    for job in jobs:
        job.logs = []
    return jobs


def get_job_detail(db: Session, job_id: UUID) -> Optional[ProductionJob]:
    job = db.query(ProductionJob).filter(ProductionJob.id == job_id).first()
    if not job:
        return None
    job.logs = db.query(ProductionLog).filter(ProductionLog.job_id == job_id).all()
    return job


def log_production_step(db: Session, job_id: UUID, log_in: ProductionLogCreate) -> ProductionLog:
    job = db.query(ProductionJob).filter(ProductionJob.id == job_id).first()
    if not job:
        raise ValueError("Job not found")
    log = ProductionLog(
        job_id=job_id,
        station_id=log_in.station_id,
        user_id=log_in.user_id,
        quantity=log_in.quantity,
    )
    db.add(log)
    job.quantity_produced += log_in.quantity
    if job.quantity_produced >= job.quantity_required:
        job.status = "COMPLETED"
    elif job.quantity_produced > 0:
        job.status = "IN_PROGRESS"
    db.commit()
    db.refresh(log)
    return log
