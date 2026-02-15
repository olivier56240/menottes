"""Add dept_code to note

Revision ID: 8e149c4cd1f4
Revises: 9ffd7cdcdf29
Create Date: 2026-02-15
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8e149c4cd1f4"
down_revision = "9ffd7cdcdf29"
branch_labels = None
depends_on = None


def upgrade():
   op.add_column("note", sa.Column("dept_code", sa.String(length=3), nullable=True))
   op.create_index("ix_note_dept_code", "note", ["dept_code"])


def downgrade():
   op.drop_index("ix_note_dept_code", table_name="note")
   op.drop_column("note", "dept_code")