"""UserProfile: delete access_token

Revision ID: c559ace41cca
Revises: dc2a8dc71324
Create Date: 2025-04-13 04:04:28.650347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c559ace41cca'
down_revision: Union[str, None] = 'dc2a8dc71324'
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
    op.add_column('user_profile', sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
