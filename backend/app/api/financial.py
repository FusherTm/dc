"""Financial accounts and transactions endpoints."""

from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.financial import (
    AccountCreate,
    AccountUpdate,
    AccountPublic,
    FinancialTransactionCreate,
    FinancialTransactionUpdate,
    FinancialTransactionPublic,
)
from app.services.financial_service import (
    create_account,
    get_account,
    get_accounts,
    update_account,
    delete_account,
    get_account_balance,
    create_transaction,
    get_transaction,
    list_transactions,
    update_transaction,
    delete_transaction,
    create_payment_for_order,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Account endpoints
# ---------------------------------------------------------------------------
accounts_router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@accounts_router.post("/", response_model=AccountPublic)
def create_account_endpoint(account_in: AccountCreate, db: Session = Depends(get_db)) -> AccountPublic:
    return create_account(db, account_in)


@accounts_router.get("/{account_id}", response_model=AccountPublic)
def read_account(account_id: UUID, db: Session = Depends(get_db)) -> AccountPublic:
    account = get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@accounts_router.get("/", response_model=List[AccountPublic])
def list_accounts(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)) -> List[AccountPublic]:
    return get_accounts(db, page, page_size)


@accounts_router.put("/{account_id}", response_model=AccountPublic)
def update_account_endpoint(account_id: UUID, account_in: AccountUpdate, db: Session = Depends(get_db)) -> AccountPublic:
    account = update_account(db, account_id, account_in)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@accounts_router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_endpoint(account_id: UUID, db: Session = Depends(get_db)) -> None:
    success = delete_account(db, account_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return None


class BalanceResponse(BaseModel):
    balance: Decimal


@accounts_router.get("/{account_id}/balance", response_model=BalanceResponse)
def account_balance(account_id: UUID, db: Session = Depends(get_db)) -> BalanceResponse:
    balance = get_account_balance(db, account_id)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return BalanceResponse(balance=balance)


# ---------------------------------------------------------------------------
# Financial transaction endpoints
# ---------------------------------------------------------------------------
transactions_router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@transactions_router.post("/", response_model=FinancialTransactionPublic)
def create_transaction_endpoint(transaction_in: FinancialTransactionCreate, db: Session = Depends(get_db)) -> FinancialTransactionPublic:
    try:
        return create_transaction(db, transaction_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@transactions_router.get("/{transaction_id}", response_model=FinancialTransactionPublic)
def read_transaction(transaction_id: UUID, db: Session = Depends(get_db)) -> FinancialTransactionPublic:
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@transactions_router.get("/", response_model=List[FinancialTransactionPublic])
def list_transactions_endpoint(
    page: int = 1,
    page_size: int = 10,
    account_id: UUID | None = None,
    direction: str | None = None,
    db: Session = Depends(get_db),
) -> List[FinancialTransactionPublic]:
    return list_transactions(db, page, page_size, account_id, direction)


@transactions_router.put("/{transaction_id}", response_model=FinancialTransactionPublic)
def update_transaction_endpoint(
    transaction_id: UUID, transaction_in: FinancialTransactionUpdate, db: Session = Depends(get_db)
) -> FinancialTransactionPublic:
    transaction = update_transaction(db, transaction_id, transaction_in)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@transactions_router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_endpoint(transaction_id: UUID, db: Session = Depends(get_db)) -> None:
    success = delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return None


# ---------------------------------------------------------------------------
# Order payment endpoint
# ---------------------------------------------------------------------------


class OrderPaymentCreate(BaseModel):
    account_id: UUID
    amount: Decimal
    description: str | None = None


@router.post("/api/orders/{order_id}/payments", response_model=FinancialTransactionPublic, tags=["orders"])
def create_payment_for_order_endpoint(
    order_id: UUID, payment_in: OrderPaymentCreate, db: Session = Depends(get_db)
) -> FinancialTransactionPublic:
    try:
        return create_payment_for_order(
            db,
            order_id=order_id,
            account_id=payment_in.account_id,
            amount=payment_in.amount,
            description=payment_in.description,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# Include sub-routers
router.include_router(accounts_router)
router.include_router(transactions_router)
