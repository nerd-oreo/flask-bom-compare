"""empty message

Revision ID: 0c79062bd2bf
Revises: 
Create Date: 2020-02-11 22:13:16.052409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c79062bd2bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_name', sa.String(length=120), nullable=False),
    sa.Column('item_type', sa.String(length=8), nullable=False),
    sa.Column('customer', sa.String(length=32), nullable=True),
    sa.Column('prefix', sa.String(length=120), nullable=True),
    sa.Column('prefix_action', sa.String(length=16), nullable=False),
    sa.Column('suffix', sa.String(length=120), nullable=True),
    sa.Column('suffix_action', sa.String(length=16), nullable=False),
    sa.Column('delimiter', sa.String(length=4), nullable=True),
    sa.Column('delimiter_action', sa.String(length=16), nullable=False),
    sa.Column('delimiter_sample', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('profile_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile')
    # ### end Alembic commands ###