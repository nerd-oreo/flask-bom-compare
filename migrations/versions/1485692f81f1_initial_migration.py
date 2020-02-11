"""Initial migration

Revision ID: 1485692f81f1
Revises: 
Create Date: 2020-02-10 19:28:48.998204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1485692f81f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('type', sa.String(length=8), nullable=False),
    sa.Column('prefix', sa.String(length=120), nullable=True),
    sa.Column('suffix', sa.String(length=120), nullable=True),
    sa.Column('delimiter', sa.String(length=4), nullable=True),
    sa.Column('action', sa.String(length=16), nullable=False),
    sa.Column('sample', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_name'), 'profile', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_profile_name'), table_name='profile')
    op.drop_table('profile')
    # ### end Alembic commands ###
