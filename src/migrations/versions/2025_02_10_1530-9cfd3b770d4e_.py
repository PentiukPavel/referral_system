"""empty message

Revision ID: 9cfd3b770d4e
Revises: e7ac84cf627a
Create Date: 2025-02-10 15:30:57.337488

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9cfd3b770d4e"
down_revision: Union[str, None] = "e7ac84cf627a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("token", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        None, "token", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "token", type_="foreignkey")
    op.drop_column("token", "user_id")
    # ### end Alembic commands ###
