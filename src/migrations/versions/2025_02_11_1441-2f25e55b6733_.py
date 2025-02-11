"""empty message

Revision ID: 2f25e55b6733
Revises: f7733cd69410
Create Date: 2025-02-11 14:41:51.492085

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f25e55b6733"
down_revision: Union[str, None] = "f7733cd69410"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "referrals",
        sa.Column("referral_id", sa.Integer(), nullable=False),
        sa.Column("referrer_id", sa.Integer(), nullable=False),
        sa.CheckConstraint("referral_id != referrer_id", name="no_self_refer"),
        sa.ForeignKeyConstraint(
            ["referral_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["referrer_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("referral_id", "referrer_id"),
        sa.UniqueConstraint(
            "referral_id", "referrer_id", name="unique_referral"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("referrals")
    # ### end Alembic commands ###
