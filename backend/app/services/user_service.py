"""Service layer for user operations."""

import uuid
from typing import Optional

from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
DEFAULT_ROLE_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        organization_id=DEFAULT_ORGANIZATION_ID,
        email=user_in.email,
        hashed_password=bcrypt.hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        role_id=DEFAULT_ROLE_ID,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not bcrypt.verify(password, user.hashed_password):
        return None
    return user
