"""initial

Revision ID: 909ec471e867
Revises: 
Create Date: 2024-09-14 15:03:51.190090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '909ec471e867'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('sex', sa.String(), nullable=False),
    sa.Column('birth_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('download',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('technology', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('tg', sa.String(), nullable=False),
    sa.Column('vk', sa.String(), nullable=False),
    sa.Column('education', sa.String(), nullable=False),
    sa.Column('work', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_subscription')
    op.drop_table('information')
    op.drop_table('download')
    op.drop_table('user')
    # ### end Alembic commands ###