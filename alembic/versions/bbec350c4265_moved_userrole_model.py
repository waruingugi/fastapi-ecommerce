"""Moved UserRole model

Revision ID: bbec350c4265
Revises: 91f0c89554bf
Create Date: 2023-02-23 15:00:45.321054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbec350c4265'
down_revision = '91f0c89554bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userrole', sa.Column('permissions', sa.Text(), nullable=True))
    op.drop_column('userrole', '_permissions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userrole', sa.Column('_permissions', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('userrole', 'permissions')
    # ### end Alembic commands ###
