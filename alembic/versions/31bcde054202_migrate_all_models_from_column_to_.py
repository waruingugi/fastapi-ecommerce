"""Migrate all models from column to mapped_column

Revision ID: 31bcde054202
Revises: 349992158dd7
Create Date: 2023-03-10 08:18:43.403347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "31bcde054202"
down_revision = "349992158dd7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
