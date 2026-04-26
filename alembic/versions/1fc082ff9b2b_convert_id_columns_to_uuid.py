"""convert id columns to uuid

Revision ID: 1fc082ff9b2b
Revises: 3ed913b68e14
Create Date: 2026-04-26 13:27:20.997976

"""
from typing import Sequence, Union

from alembic import op


revision: str = '1fc082ff9b2b'
down_revision: Union[str, Sequence[str], None] = '3ed913b68e14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('messages_conversation_id_fkey', 'messages', type_='foreignkey')

    op.execute('ALTER TABLE conversations ALTER COLUMN id TYPE uuid USING id::uuid')
    op.execute('ALTER TABLE messages ALTER COLUMN id TYPE uuid USING id::uuid')
    op.execute('ALTER TABLE messages ALTER COLUMN conversation_id TYPE uuid USING conversation_id::uuid')

    op.create_foreign_key(
        'messages_conversation_id_fkey',
        'messages', 'conversations',
        ['conversation_id'], ['id'],
    )
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_constraint('messages_conversation_id_fkey', 'messages', type_='foreignkey')

    op.execute('ALTER TABLE messages ALTER COLUMN conversation_id TYPE varchar USING conversation_id::text')
    op.execute('ALTER TABLE messages ALTER COLUMN id TYPE varchar USING id::text')
    op.execute('ALTER TABLE conversations ALTER COLUMN id TYPE varchar USING id::text')

    op.create_foreign_key(
        'messages_conversation_id_fkey',
        'messages', 'conversations',
        ['conversation_id'], ['id'],
    )
