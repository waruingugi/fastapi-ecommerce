"""Remove country relationship in BusinessPartner model

Revision ID: c965dfb7e3b2
Revises: b457c3be5051
Create Date: 2023-03-15 00:50:43.213044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c965dfb7e3b2"
down_revision = "b457c3be5051"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "businesspartner_country_id_fkey", "businesspartner", type_="foreignkey"
    )
    op.drop_column("businesspartner", "country_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "businesspartner",
        sa.Column("country_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "businesspartner_country_id_fkey",
        "businesspartner",
        "country",
        ["country_id"],
        ["id"],
    )
    # ### end Alembic commands ###
