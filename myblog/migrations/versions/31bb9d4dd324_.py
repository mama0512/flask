"""empty message

Revision ID: 31bb9d4dd324
Revises: b6a03f19bda6
Create Date: 2021-01-02 17:59:03.684256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31bb9d4dd324'
down_revision = 'b6a03f19bda6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
