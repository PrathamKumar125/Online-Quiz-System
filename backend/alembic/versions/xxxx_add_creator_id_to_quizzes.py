"""add creator_id to quizzes

Revision ID: xxxx
Revises: 
Create Date: 2023-10-10

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '01'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('quizzes') as batch_op:
        batch_op.add_column(sa.Column('creator_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_quizzes_creator_id_users', 'users', ['creator_id'], ['id'])

def downgrade():
    with op.batch_alter_table('quizzes') as batch_op:
        batch_op.drop_constraint('fk_quizzes_creator_id_users', type_='foreignkey')
        batch_op.drop_column('creator_id')
