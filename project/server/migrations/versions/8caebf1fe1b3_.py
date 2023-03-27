"""empty message

Revision ID: 8caebf1fe1b3
Revises: f435d4ffda49
Create Date: 2023-03-27 23:23:46.684653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8caebf1fe1b3'
down_revision = 'f435d4ffda49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('export_job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('export_job', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    # ### end Alembic commands ###
