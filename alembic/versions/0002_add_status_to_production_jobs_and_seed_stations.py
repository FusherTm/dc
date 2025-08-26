"""add status to production jobs and seed stations"""

from alembic import op
import sqlalchemy as sa
import uuid

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

DEFAULT_ORGANIZATION_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
STATIONS = [
    ("Cam Kesim", "CAM_KESIM", 1),
    ("Pres", "PRES", 2),
]


def upgrade() -> None:
    op.add_column(
        "production_jobs",
        sa.Column("status", sa.String(length=50), server_default="PENDING", nullable=False),
    )
    for name, code, order_index in STATIONS:
        op.execute(
            sa.text(
                "INSERT INTO production_stations (id, organization_id, name, code, order_index) "
                "SELECT :id, :org, :name, :code, :order_index "
                "WHERE NOT EXISTS (SELECT 1 FROM production_stations WHERE code=:code)"
            ),
            {
                "id": str(uuid.uuid4()),
                "org": str(DEFAULT_ORGANIZATION_ID),
                "name": name,
                "code": code,
                "order_index": order_index,
            },
        )


def downgrade() -> None:
    op.drop_column("production_jobs", "status")
    for _, code, _ in STATIONS:
        op.execute(sa.text("DELETE FROM production_stations WHERE code=:code"), {"code": code})
