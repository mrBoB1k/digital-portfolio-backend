"""change additional info

Revision ID: c55a5d1812b3
Revises: e1f476164346
Create Date: 2024-04-24 17:40:10.178178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c55a5d1812b3'
down_revision: Union[str, None] = 'e1f476164346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('information', sa.Column('technology', sa.ARRAY(sa.String()), nullable=False))
    op.add_column('information', sa.Column('tg', sa.String(), nullable=False))
    op.add_column('information', sa.Column('vk', sa.String(), nullable=False))
    op.drop_column('information', 'telegram')
    op.drop_column('information', 'additional_information')
    op.drop_column('information', 'vkontakte')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('information', sa.Column('vkontakte', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('information', sa.Column('additional_information', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('information', sa.Column('telegram', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('information', 'vk')
    op.drop_column('information', 'tg')
    op.drop_column('information', 'technology')
    # ### end Alembic commands ###
