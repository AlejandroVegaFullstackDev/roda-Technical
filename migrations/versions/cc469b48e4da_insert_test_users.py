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
    conn = op.get_bind()

    # la contraseña plana que quieres hashear:
    plain = b'12345'
    # genera dos salts distintos para juan y maria
    hash_juan  = bcrypt.hashpw(plain, bcrypt.gensalt()).decode('utf-8')
    hash_maria = bcrypt.hashpw(plain, bcrypt.gensalt()).decode('utf-8')

    # inserta los usuarios con los hashes
    conn.execute(text("""
        INSERT INTO usuarios (username, password_hash, role_id)
        VALUES
          (:juan,  :hash_juan,  3),
          (:maria, :hash_maria, 2)
    """), {
        "juan": "juan",  "hash_juan":  hash_juan,
        "maria": "maria","hash_maria": hash_maria
    })
def downgrade():
    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("DELETE FROM usuarios WHERE username IN ('juan', 'maria');"))
