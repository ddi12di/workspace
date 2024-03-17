"""init

Revision ID: 5d241216e60e
Revises: b551a76751e5
Create Date: 2024-03-11 16:22:54.164746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d241216e60e'
down_revision: Union[str, None] = 'b551a76751e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db1',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_db1_body'), 'db1', ['body'], unique=False)
    op.create_index(op.f('ix_db1_title'), 'db1', ['title'], unique=False)
    op.create_index(op.f('ix_db1_user_id'), 'db1', ['user_id'], unique=False)
    op.drop_index('ix_people_body', table_name='people')
    op.drop_index('ix_people_title', table_name='people')
    op.drop_index('ix_people_user_id', table_name='people')
    op.drop_table('people')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('body', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='people_pkey')
    )
    op.create_index('ix_people_user_id', 'people', ['user_id'], unique=False)
    op.create_index('ix_people_title', 'people', ['title'], unique=False)
    op.create_index('ix_people_body', 'people', ['body'], unique=False)
    op.drop_index(op.f('ix_db1_user_id'), table_name='db1')
    op.drop_index(op.f('ix_db1_title'), table_name='db1')
    op.drop_index(op.f('ix_db1_body'), table_name='db1')
    op.drop_table('db1')
    # ### end Alembic commands ###
