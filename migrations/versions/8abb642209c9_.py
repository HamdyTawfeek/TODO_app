"""empty message

Revision ID: 8abb642209c9
Revises: b6375aeb7e3d
Create Date: 2020-04-19 10:18:03.746305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8abb642209c9'
down_revision = 'b6375aeb7e3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    op.execute('UPDATE todos SET completed = False WHERE completed is NULL;')
    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
