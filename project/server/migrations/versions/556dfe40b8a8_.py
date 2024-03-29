"""empty message

Revision ID: 556dfe40b8a8
Revises: fb80e6e78193
Create Date: 2023-02-26 23:47:59.109551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556dfe40b8a8'
down_revision = 'fb80e6e78193'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('post')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post', sa.INTEGER(), nullable=False))
        batch_op.drop_column('post_id')

    # ### end Alembic commands ###
