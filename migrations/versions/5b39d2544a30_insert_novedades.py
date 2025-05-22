"""insert novedades

Revision ID: 5b39d2544a30
Revises: a6f2e7ada5d4
Create Date: 2025-05-22 00:19:53.085165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b39d2544a30'
down_revision = 'a6f2e7ada5d4'
branch_labels = None
depends_on = None


def upgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO novedades (id, nombre) VALUES
        (1, 'Disponible'),
        (2, 'No Disponible');
    """))

def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM novedades WHERE id IN (1,2);"))
