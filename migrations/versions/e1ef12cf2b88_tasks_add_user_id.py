"""Tasks: add user_id

Revision ID: e1ef12cf2b88
Revises: c559ace41cca
Create Date: 2025-04-13 08:05:43.632436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1ef12cf2b88'
down_revision: Union[str, None] = 'c559ace41cca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tasks', 'user_profile', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')
    # ### end Alembic commands ###
