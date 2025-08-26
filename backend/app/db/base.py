"""Base class for SQLAlchemy models and model imports for Alembic."""

from sqlalchemy.orm import declarative_base


Base = declarative_base()


# Import all model classes so that Alembic can detect them via Base.metadata
# noqa: F401
from app.models import (  # type: ignore  # pylint: disable=unused-import
    Account,
    FinancialTransaction,
    Material,
    Order,
    OrderItem,
    Organization,
    Partner,
    Product,
    ProductionJob,
    ProductionLog,
    ProductionStation,
    PurchaseOrder,
    PurchaseOrderItem,
    Role,
    User,
)

