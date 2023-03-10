"""Add country_id fk to user model

Revision ID: b63bbb5b2a5f
Revises: 2e7b844e8ef1
Create Date: 2023-03-11 16:05:54.604059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b63bbb5b2a5f"
down_revision = "2e7b844e8ef1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("country_id", sa.String(), nullable=True))
    op.create_foreign_key(None, "user", "country", ["country_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_column("user", "country_id")
    # ### end Alembic commands ###
