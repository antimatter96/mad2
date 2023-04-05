"""empty message

Revision ID: 964537a613a2
Revises: 8ef65df432a6
Create Date: 2023-04-06 02:52:33.849751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '964537a613a2'
down_revision = '8ef65df432a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_last_seen', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rand_number', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_last_seen', schema=None) as batch_op:
        batch_op.drop_column('rand_number')

    # ### end Alembic commands ###
