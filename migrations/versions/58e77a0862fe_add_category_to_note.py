"""add category to note

Revision ID: 58e77a0862fe
Revises: 9667c99da1d6
Create Date: 2026-02-06 08:18:39.879989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58e77a0862fe'
down_revision = '9667c99da1d6'
branch_labels = None
depends_on = None

def upgrade():
   # 1) Ajouter la colonne en nullable + default temporaire
   op.add_column(
       "note",
       sa.Column("category", sa.String(length=30), nullable=True, server_default="voiture"),
   )

   # 2) Remplir les anciennes lignes
   op.execute("UPDATE note SET category = 'voiture' WHERE category IS NULL")

   # 3) Enlever le default puis forcer NOT NULL
   op.alter_column("note", "category", server_default=None)
   op.alter_column("note", "category", nullable=False)


def downgrade():
   op.drop_column("note", "category")

    # ### end Alembic commands ###
