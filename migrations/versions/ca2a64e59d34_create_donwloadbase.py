"""create donwloadbase

Revision ID: ca2a64e59d34
Revises: 06bc783f331f
Create Date: 2024-04-27 19:42:08.524649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2a64e59d34'
down_revision: Union[str, None] = '06bc783f331f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('download',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('download')
    # ### end Alembic commands ###
