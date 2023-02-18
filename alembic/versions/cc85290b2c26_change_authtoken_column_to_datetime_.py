"""Change authtoken column to datetime field

Revision ID: cc85290b2c26
Revises: daefc1309af9
Create Date: 2023-02-18 23:10:59.790386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = 'cc85290b2c26'
down_revision = 'daefc1309af9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authtoken', sa.Column('refresh_token_expires_at', sa.DateTime(), nullable=False, server_default=func.now()))
    op.drop_column('authtoken', 'refresh_token_expires_in')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authtoken', sa.Column('refresh_token_expires_in', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.drop_column('authtoken', 'refresh_token_expires_at')
    # ### end Alembic commands ###