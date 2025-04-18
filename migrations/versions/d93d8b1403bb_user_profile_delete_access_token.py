"""user_profile delete access_token

Revision ID: d93d8b1403bb
Revises: 2b3b706226c1
Create Date: 2025-04-10 01:39:59.374358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd93d8b1403bb'
down_revision: Union[str, None] = '2b3b706226c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'access_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
