"""Service layer for financial operations."""

import uuid
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.financial_transaction import FinancialTransaction
from app.models.order import Order
from app.schemas.financial import (
    AccountCreate,
    AccountUpdate,
    FinancialTransactionCreate,
    FinancialTransactionUpdate,
)

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


# ---------------------------------------------------------------------------
# Account operations
# ---------------------------------------------------------------------------

def create_account(db: Session, account_in: AccountCreate) -> Account:
    account = Account(
        organization_id=DEFAULT_ORGANIZATION_ID,
        name=account_in.name,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account(db: Session, account_id: UUID) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()


def get_accounts(db: Session, page: int = 1, page_size: int = 10) -> List[Account]:
    return db.query(Account).offset((page - 1) * page_size).limit(page_size).all()


def update_account(db: Session, account_id: UUID, account_in: AccountUpdate) -> Optional[Account]:
    account = get_account(db, account_id)
    if not account:
        return None
    for field, value in account_in.dict(exclude_unset=True).items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, account_id: UUID) -> bool:
    account = get_account(db, account_id)
    if not account:
        return False
    db.delete(account)
    db.commit()
    return True


def get_account_balance(db: Session, account_id: UUID) -> Optional[Decimal]:
    account = get_account(db, account_id)
    if not account:
        return None
    return Decimal(account.current_balance)


# ---------------------------------------------------------------------------
# Financial transaction operations
# ---------------------------------------------------------------------------

def _apply_transaction_to_account(account: Account, direction: str, amount: Decimal) -> None:
    if direction == "IN":
        account.current_balance = Decimal(account.current_balance) + amount
    else:
        account.current_balance = Decimal(account.current_balance) - amount


def create_transaction(
    db: Session, transaction_in: FinancialTransactionCreate
) -> FinancialTransaction:
    account = get_account(db, transaction_in.account_id)
    if not account:
        raise ValueError("Account not found")
    transaction = FinancialTransaction(
        organization_id=DEFAULT_ORGANIZATION_ID,
        account_id=transaction_in.account_id,
        partner_id=transaction_in.partner_id,
        order_id=transaction_in.order_id,
        purchase_order_id=transaction_in.purchase_order_id,
        direction=transaction_in.direction,
        amount=transaction_in.amount,
        description=transaction_in.description,
    )
    db.add(transaction)
    _apply_transaction_to_account(account, transaction.direction, transaction.amount)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transaction(db: Session, transaction_id: UUID) -> Optional[FinancialTransaction]:
    return db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()


def list_transactions(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    account_id: UUID | None = None,
    direction: str | None = None,
) -> List[FinancialTransaction]:
    query = db.query(FinancialTransaction)
    if account_id:
        query = query.filter(FinancialTransaction.account_id == account_id)
    if direction:
        query = query.filter(FinancialTransaction.direction == direction)
    return query.offset((page - 1) * page_size).limit(page_size).all()


def update_transaction(
    db: Session, transaction_id: UUID, transaction_in: FinancialTransactionUpdate
) -> Optional[FinancialTransaction]:
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return None
    # Reverse old effect on account
    account = get_account(db, transaction.account_id)
    _apply_transaction_to_account(account, "OUT" if transaction.direction == "IN" else "IN", transaction.amount)
    for field, value in transaction_in.dict(exclude_unset=True).items():
        setattr(transaction, field, value)
    # Apply new effect
    _apply_transaction_to_account(account, transaction.direction, transaction.amount)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction_id: UUID) -> bool:
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return False
    account = get_account(db, transaction.account_id)
    _apply_transaction_to_account(account, "OUT" if transaction.direction == "IN" else "IN", transaction.amount)
    db.delete(transaction)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Business operations
# ---------------------------------------------------------------------------

def create_payment_for_order(
    db: Session,
    order_id: UUID,
    account_id: UUID,
    amount: Decimal,
    description: str | None = None,
) -> FinancialTransaction:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")
    transaction_in = FinancialTransactionCreate(
        account_id=account_id,
        order_id=order_id,
        direction="IN",
        amount=amount,
        description=description,
    )
    transaction = create_transaction(db, transaction_in)
    # Update order status
    order.status = "TESLIM EDILDI"
    db.commit()
    db.refresh(order)
    return transaction
