"""insert roles

Revision ID: 7bdf646953d3
Revises: 
Create Date: 2025-05-22 00:19:35.953576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bdf646953d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO roles (id, nombre) VALUES
        (1, 'admin'),
        (2, 'operador'),
        (3, 'cliente');
    """))

def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM roles WHERE id IN (1,2,3);"))
