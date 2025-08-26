"""add status to production jobs and seed stations"""
from alembic import op
import sqlalchemy as sa
import uuid

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

DEFAULT_ORGANIZATION_ID = str(uuid.UUID("00000000-0000-0000-0000-000000000001"))
DEFAULT_ORGANIZATION_NAME = "Default Org"
DEFAULT_ORGANIZATION_SLUG = "default-org"

STATIONS = [
    ("Cam Kesim", "CAM_KESIM", 1),
    ("Pres", "PRES", 2),
]

def execp(sql: str, params: dict | None = None):
    conn = op.get_bind()
    if params:
        conn.execute(sa.text(sql), params)
    else:
        conn.execute(sa.text(sql))

def upgrade() -> None:
    # 1) production_jobs.status kolonu
    op.add_column(
        "production_jobs",
        sa.Column("status", sa.String(length=50), server_default="PENDING", nullable=False),
    )

    # 2) organization: varsa ilkini kullan; yoksa default ekle
    conn = op.get_bind()
    org_id = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1")).scalar()
    if not org_id:
        org_id = DEFAULT_ORGANIZATION_ID
        execp(
            """
            INSERT INTO organizations (id, name, slug)
            VALUES (:id, :name, :slug)
            ON CONFLICT (id) DO NOTHING
            """,
            {"id": org_id, "name": DEFAULT_ORGANIZATION_NAME, "slug": DEFAULT_ORGANIZATION_SLUG},
        )

    # 3) istasyon seed (yoksa ekle)
    for name, code, order_index in STATIONS:
        execp(
            """
            INSERT INTO production_stations (id, organization_id, name, code, order_index)
            SELECT :id, :org, :name, :code, :order_index
            WHERE NOT EXISTS (SELECT 1 FROM production_stations WHERE code = :code)
            """,
            {
                "id": str(uuid.uuid4()),
                "org": str(org_id),
                "name": name,
                "code": code,
                "order_index": order_index,
            },
        )

def downgrade() -> None:
    op.drop_column("production_jobs", "status")
    for _, code, _ in STATIONS:
        execp("DELETE FROM production_stations WHERE code = :code", {"code": code})
