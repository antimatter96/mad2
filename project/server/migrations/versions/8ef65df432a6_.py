"""empty message

Revision ID: 8ef65df432a6
Revises: 726ef972605b
Create Date: 2023-03-29 04:07:51.771653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ef65df432a6'
down_revision = '726ef972605b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_last_seen',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_seen_at', sa.DATETIME(), nullable=True))

    op.drop_table('users_last_seen')
    # ### end Alembic commands ###
