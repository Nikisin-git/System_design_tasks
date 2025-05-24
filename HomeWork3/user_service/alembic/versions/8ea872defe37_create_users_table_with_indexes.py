"""Create users table with indexes

Revision ID: 8ea872defe37
Revises: 
Create Date: 2025-05-22 14:34:51.205955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8ea872defe37'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('full_name', sa.String(length=200), nullable=False),
    sa.Column('login', sa.String(length=200), nullable=False),
    sa.Column('hashed_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index(op.f('ix_users_full_name'), 'users', ['full_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_full_name'), table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')