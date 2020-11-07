"""empty message

Revision ID: cccc48a5eac8
Revises: c27ceee55648
Create Date: 2020-11-07 07:27:44.578914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cccc48a5eac8'
down_revision = 'c27ceee55648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('tokenid', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('tokenid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###
