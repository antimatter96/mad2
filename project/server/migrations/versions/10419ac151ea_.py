"""empty message

Revision ID: 10419ac151ea
Revises: 556dfe40b8a8
Create Date: 2023-03-21 23:37:14.255475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10419ac151ea'
down_revision = '556dfe40b8a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('img_url',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('img_url',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
