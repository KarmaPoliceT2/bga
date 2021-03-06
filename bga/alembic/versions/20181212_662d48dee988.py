"""Revise

Revision ID: 662d48dee988
Revises: 6109f7fb5199
Create Date: 2018-12-12 02:46:24.783787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662d48dee988'
down_revision = '6109f7fb5199'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False),
    sa.Column('password', sa.Unicode(length=255), nullable=False),
    sa.Column('pubkey', sa.String(), nullable=False),
    sa.Column('privkey', sa.String(), nullable=False),
    sa.Column('last_logged', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('name', name=op.f('uq_users_name'))
    )
    op.drop_index('my_index', table_name='models')
    op.drop_table('models')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('models',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=True),
    sa.Column('value', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_models')
    )
    op.create_index('my_index', 'models', ['name'], unique=1)
    op.drop_table('users')
    # ### end Alembic commands ###
