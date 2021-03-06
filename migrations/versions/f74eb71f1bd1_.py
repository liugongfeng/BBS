"""empty message

Revision ID: f74eb71f1bd1
Revises: 9b6d01a93d83
Create Date: 2019-04-30 13:52:46.108924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74eb71f1bd1'
down_revision = '9b6d01a93d83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.String(length=100), nullable=False))
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###
