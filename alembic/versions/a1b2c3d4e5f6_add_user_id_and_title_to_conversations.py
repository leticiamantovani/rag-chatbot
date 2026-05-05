"""add user_id and title to conversations

Revision ID: a1b2c3d4e5f6
Revises: f327a9265f4c
Create Date: 2026-05-03 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'a1b2c3d4e5f6'
down_revision = 'f327a9265f4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('conversations', sa.Column('user_id', UUID(as_uuid=True), nullable=True))
    op.add_column('conversations', sa.Column('title', sa.String(255), nullable=True))
    op.create_foreign_key(
        'fk_conversations_user_id',
        'conversations', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_constraint('fk_conversations_user_id', 'conversations', type_='foreignkey')
    op.drop_column('conversations', 'title')
    op.drop_column('conversations', 'user_id')
