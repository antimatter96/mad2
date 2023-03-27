"""empty message

Revision ID: aa6fbafbc732
Revises: 92f9748d02f9
Create Date: 2023-03-27 21:16:25.328084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa6fbafbc732'
down_revision = '92f9748d02f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('export_job',
    sa.Column('job_id', sa.String(), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('error', sa.Boolean(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('job_id', 'file_path')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('export_job')
    # ### end Alembic commands ###
