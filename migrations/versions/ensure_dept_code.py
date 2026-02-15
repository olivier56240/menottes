"""ensure dept_code on note

Revision ID: ensure_dept_code_01
Revises: 8ef4149c4cd1
Create Date: 2026-02-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# ⚠️ IMPORTANT : remplace down_revision par la dernière révision de TON dossier versions/
revision = "ensure_dept_code_01"
down_revision = "<MET_ICI_LA_DERNIERE_REVISION_EXISTANTE>"
branch_labels = None
depends_on = None


def _has_column(table_name: str, col_name: str) -> bool:
   bind = op.get_bind()
   insp = inspect(bind)
   cols = [c["name"] for c in insp.get_columns(table_name)]
   return col_name in cols


def upgrade():
   # Table = "note" (d’après ton log SQL : FROM note)
   if not _has_column("note", "dept_code"):
       with op.batch_alter_table("note") as batch_op:
           batch_op.add_column(sa.Column("dept_code", sa.String(length=3), nullable=True))

       # (optionnel) index pour filtrer vite par dept
       # ⚠️ évite doublon si index existe déjà
       bind = op.get_bind()
       insp = inspect(bind)
       indexes = [i["name"] for i in insp.get_indexes("note")]
       if "ix_note_dept_code" not in indexes:
           op.create_index("ix_note_dept_code", "note", ["dept_code"])


def downgrade():
   # On retire seulement si existe
   if _has_column("note", "dept_code"):
       with op.batch_alter_table("note") as batch_op:
           batch_op.drop_column("dept_code")