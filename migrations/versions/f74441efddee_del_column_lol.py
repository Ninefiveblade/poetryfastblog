"""del column lol

Revision ID: f74441efddee
Revises: 64a6c8e11ce0
Create Date: 2022-05-25 15:35:11.166498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74441efddee'
down_revision = '64a6c8e11ce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("lol")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lol', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
