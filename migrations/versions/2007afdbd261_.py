"""empty message

Revision ID: 2007afdbd261
Revises: d5b125d465fe
Create Date: 2019-05-01 16:06:38.590343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2007afdbd261'
down_revision = 'd5b125d465fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('highlight_post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('highlight_post')
    # ### end Alembic commands ###
