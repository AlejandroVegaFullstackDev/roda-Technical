"""insert estados

Revision ID: a6f2e7ada5d4
Revises: cc469b48e4da
Create Date: 2025-05-22 00:19:48.378317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6f2e7ada5d4'
down_revision = 'cc469b48e4da'
branch_labels = None
depends_on = None


def upgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO estados (id, nombre, descripcion) VALUES
        (1, 'Disponible', 'Disponible/Desbloqueado/estado libre'),
        (2, 'Robo', 'Bloqueado por robo'),
        (3, 'Falta de Pago', 'Bloqueado por falta de pago');
    """))

def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM estados WHERE id IN (1,2,3);"))
