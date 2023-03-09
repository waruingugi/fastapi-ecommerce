"""Set cascade on delete for UserRole model

Revision ID: 7589b3275af5
Revises: 2d33649a39e0
Create Date: 2023-03-09 14:20:49.801357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7589b3275af5"
down_revision = "2d33649a39e0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("userrole_role_id_fkey", "userrole", type_="foreignkey")
    op.drop_constraint("userrole_user_id_fkey", "userrole", type_="foreignkey")
    op.create_foreign_key(
        None, "userrole", "role", ["role_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "userrole", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "userrole", type_="foreignkey")
    op.drop_constraint(None, "userrole", type_="foreignkey")
    op.create_foreign_key(
        "userrole_user_id_fkey", "userrole", "user", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "userrole_role_id_fkey", "userrole", "role", ["role_id"], ["id"]
    )
    # ### end Alembic commands ###
