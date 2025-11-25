"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create exchange_rates table
    op.create_table('exchange_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_currency', sa.String(length=3), nullable=False),
    sa.Column('to_currency', sa.String(length=3), nullable=False),
    sa.Column('period', sa.String(length=10), nullable=False),
    sa.Column('rate', sa.Numeric(precision=18, scale=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('from_currency', 'to_currency', 'period', name='uq_exchange_rate')
    )
    op.create_index(op.f('ix_exchange_rates_id'), 'exchange_rates', ['id'], unique=False)
    op.create_index(op.f('ix_exchange_rates_from_currency'), 'exchange_rates', ['from_currency'], unique=False)
    op.create_index(op.f('ix_exchange_rates_to_currency'), 'exchange_rates', ['to_currency'], unique=False)
    op.create_index(op.f('ix_exchange_rates_period'), 'exchange_rates', ['period'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_exchange_rates_period'), table_name='exchange_rates')
    op.drop_index(op.f('ix_exchange_rates_to_currency'), table_name='exchange_rates')
    op.drop_index(op.f('ix_exchange_rates_from_currency'), table_name='exchange_rates')
    op.drop_index(op.f('ix_exchange_rates_id'), table_name='exchange_rates')
    op.drop_table('exchange_rates')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

