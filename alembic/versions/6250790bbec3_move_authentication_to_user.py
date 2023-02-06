"""move authentication to user

Revision ID: 6250790bbec3
Revises: 61a455229eb5
Create Date: 2023-02-06 12:31:20.020759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6250790bbec3'
down_revision = '61a455229eb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        table_name="user", column_name="password",
        new_column_name="hashed_password", type_=sa.String(),
        nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        table_name="user", column_name="hashed_password",
        new_column_name="password", type_=sa.String(),
        nullable=False
    )
