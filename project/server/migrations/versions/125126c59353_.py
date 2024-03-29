"""empty message

Revision ID: 125126c59353
Revises: 964537a613a2
Create Date: 2023-04-06 04:15:46.749251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '125126c59353'
down_revision = '964537a613a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    # ### end Alembic commands ###
