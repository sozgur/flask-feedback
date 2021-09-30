"""Initial migration.

Revision ID: 39a7c89ca2e8
Revises: 
Create Date: 2021-09-29 20:49:32.335607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39a7c89ca2e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('email')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedbacks')
    op.drop_table('users')
    # ### end Alembic commands ###
