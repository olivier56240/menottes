"""Merge heads

Revision ID: e1e09bc2a888
Revises: 8ef4149c4cd1, ensure_dept_code_01
Create Date: 2026-02-15 16:29:00.897152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1e09bc2a888'
down_revision = ('8ef4149c4cd1', 'ensure_dept_code_01')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
