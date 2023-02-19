"""Rename Authtoken model columns; rename TokenCreate serializer fields

Revision ID: a92014f5dd9d
Revises: cc85290b2c26
Create Date: 2023-02-19 09:13:24.239137

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision = 'a92014f5dd9d'
down_revision = 'cc85290b2c26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authtoken', sa.Column('access_token_eat', sa.DateTime(), nullable=False, server_default=func.now()))
    op.add_column('authtoken', sa.Column('refresh_token_eat', sa.DateTime(), nullable=False, server_default=func.now()))
    op.drop_column('authtoken', 'access_token_expires_at')
    op.drop_column('authtoken', 'refresh_token_expires_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authtoken', sa.Column('refresh_token_expires_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('authtoken', sa.Column('access_token_expires_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('authtoken', 'refresh_token_eat')
    op.drop_column('authtoken', 'access_token_eat')
    # ### end Alembic commands ###
