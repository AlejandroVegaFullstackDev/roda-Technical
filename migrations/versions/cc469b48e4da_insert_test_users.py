"""insert test users

Revision ID: cc469b48e4da
Revises: 7bdf646953d3
Create Date: 2025-05-22 00:19:43.096405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc469b48e4da'
down_revision = '7bdf646953d3'
branch_labels = None
depends_on = None


def upgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO usuarios (username, password_base64, role_id) VALUES
        ('juan', encode(convert_to('12345', 'UTF8'), 'base64'), 3),
        ('maria', encode(convert_to('12345', 'UTF8'), 'base64'), 2);
    """))

def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM usuarios WHERE username IN ('juan', 'maria');"))
