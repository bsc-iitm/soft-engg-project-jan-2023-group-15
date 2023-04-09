"""empty message

Revision ID: 5ea686b834ee
Revises: 3ce5ddf9cde0
Create Date: 2023-04-09 14:38:02.954791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ea686b834ee'
down_revision = '3ce5ddf9cde0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faqs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved_by_id', sa.Text(), nullable=False))
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=7),
               type_=sa.Enum('REQUESTED', 'ACTIVE', 'DELETED', name='status'),
               existing_nullable=True,
               existing_server_default=sa.text("'ACTIVE'"))
        batch_op.create_foreign_key(None, 'user', ['approved_by_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faqs', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('status',
               existing_type=sa.Enum('REQUESTED', 'ACTIVE', 'DELETED', name='status'),
               type_=sa.VARCHAR(length=7),
               existing_nullable=True,
               existing_server_default=sa.text("'ACTIVE'"))
        batch_op.drop_column('approved_by_id')

    # ### end Alembic commands ###