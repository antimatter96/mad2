"""empty message

Revision ID: fb80e6e78193
Revises: 41ce9b2c821c
Create Date: 2023-02-26 23:47:25.699725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb80e6e78193'
down_revision = '41ce9b2c821c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_url', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('hidden', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('hidden')
        batch_op.drop_column('img_url')

    # ### end Alembic commands ###
