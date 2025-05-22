"""insert novedades-estados map

Revision ID: 49df1b066d4b
Revises: 5b39d2544a30
Create Date: 2025-05-22 00:20:01.757726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49df1b066d4b'
down_revision = '5b39d2544a30'
branch_labels = None
depends_on = None


def upgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO novedades_estados (novedad_id, estado_id) VALUES
        (1, 1),
        (2, 2),
        (2, 3);
    """))

def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM novedades_estados WHERE (novedad_id = 1 AND estado_id = 1) OR (novedad_id = 2 AND estado_id IN (2,3));"))
