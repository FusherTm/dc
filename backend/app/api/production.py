"""Production job and log endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.production import (
    ProductionJobPublic,
    ProductionLogCreate,
    ProductionLogPublic,
)
from app.services.production_service import (
    get_jobs,
    get_job_detail,
    log_production_step,
)

router = APIRouter(prefix="/api/production", tags=["production"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/jobs", response_model=List[ProductionJobPublic])
def list_jobs(
    page: int = 1,
    page_size: int = 10,
    status: str | None = None,
    db: Session = Depends(get_db),
) -> List[ProductionJobPublic]:
    return get_jobs(db, page, page_size, status)


@router.get("/jobs/{job_id}", response_model=ProductionJobPublic)
def read_job(job_id: UUID, db: Session = Depends(get_db)) -> ProductionJobPublic:
    job = get_job_detail(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.post("/jobs/{job_id}/logs", response_model=ProductionLogPublic)
def create_log(
    job_id: UUID, log_in: ProductionLogCreate, db: Session = Depends(get_db)
) -> ProductionLogPublic:
    try:
        return log_production_step(db, job_id, log_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
