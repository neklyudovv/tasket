"""initial

Revision ID: 3b6a89fcc3eb
Revises: 
Create Date: 2025-07-23 23:24:03.148793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b6a89fcc3eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('users_tg_id_key'), 'users', type_='unique')
    op.drop_column('users', 'tg_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_unique_constraint(op.f('users_tg_id_key'), 'users', ['tg_id'], postgresql_nulls_not_distinct=False)
    # ### end Alembic commands ###
