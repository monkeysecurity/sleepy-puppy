"""empty message

Revision ID: 16a92c216f4c
Revises: 2334b4d3b7be
Create Date: 2015-08-12 10:53:07.306964

"""

# revision identifiers, used by Alembic.
revision = '16a92c216f4c'
down_revision = '2334b4d3b7be'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('captures', sa.Column('returns', sa.TEXT(), nullable=True))
    ### end Alembic commands ###