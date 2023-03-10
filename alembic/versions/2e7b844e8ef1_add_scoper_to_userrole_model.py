"""Add scoper to UserRole model

Revision ID: 2e7b844e8ef1
Revises: 0197809287c7
Create Date: 2023-03-11 11:24:52.073423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2e7b844e8ef1"
down_revision = "0197809287c7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "userrole",
        sa.Column(
            "scope", postgresql.ARRAY(sa.String()), server_default="{}", nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("userrole", "scope")
    # ### end Alembic commands ###
