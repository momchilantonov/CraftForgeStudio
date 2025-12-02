"""add hierarchical categories

Revision ID: c118cbc0717e
Revises: 9517da0867ac
Create Date: 2025-12-02

"""
from alembic import op
import sqlalchemy as sa


revision = 'c118cbc0717e'
down_revision = '9517da0867ac'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('level', sa.Integer(),
                            nullable=False, server_default='0'))
        batch_op.create_index(batch_op.f('ix_categories_parent_id'), [
                              'parent_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_categories_parent_id', 'categories', ['parent_id'], ['id'])


def downgrade():
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint('fk_categories_parent_id', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_categories_parent_id'))
        batch_op.drop_column('level')
        batch_op.drop_column('parent_id')
