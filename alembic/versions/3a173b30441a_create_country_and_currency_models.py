"""Create Country and Currency models

Revision ID: 3a173b30441a
Revises: 0f3baa74c56e
Create Date: 2023-03-08 14:03:21.406081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a173b30441a"
down_revision = "0f3baa74c56e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "country",
        sa.Column("dialing_code", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("iso2_code", sa.String(), nullable=True),
        sa.Column("iso3_code", sa.String(), nullable=True),
        sa.Column("currency_id", sa.String(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currency.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dialing_code"),
        sa.UniqueConstraint("iso2_code"),
        sa.UniqueConstraint("iso3_code"),
        sa.UniqueConstraint("name"),
    )
    op.alter_column(
        "businesspartner", "owner_id", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "businesspartner", "owner_id", existing_type=sa.VARCHAR(), nullable=True
    )
    op.drop_table("country")
    op.drop_table("currency")
    # ### end Alembic commands ###
