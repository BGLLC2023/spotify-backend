"""update april27

Revision ID: 59747f4d4747
Revises: a5fd10c36146
Create Date: 2026-04-27 10:13:29.713966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59747f4d4747'
down_revision: Union[str, Sequence[str], None] = 'a5fd10c36146'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('spotify_users') as batch_op:
        batch_op.add_column(sa.Column('country_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_spotify_users_country', 'countries', ['country_id'], ['country_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table('spotify_users') as batch_op:
        batch_op.drop_constraint('fk_spotify_users_country', type_='foreignkey')
        batch_op.drop_column('country_id')
    # ### end Alembic commands ###
