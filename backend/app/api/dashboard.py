# app/api/dashboard.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/finance/summary")
def finance_summary():
    return {"revenue": 125000, "expense": 83000, "profit": 42000, "currency": "TRY"}

@router.get("/operations/summary")
def operations_summary():
    return {"orders_pending": 7, "orders_in_progress": 12, "orders_completed_today": 5, "stations_active": 2}
