"""empty message

Revision ID: 27088205bb83
Revises: 
Create Date: 2025-08-20 13:31:57.693549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27088205bb83'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    with op.batch_alter_table('category') as batch:
        batch.add_column(sa.Column('name', sa.String(length=50), nullable=True))


    conn = op.get_bind()
    conn.execute(sa.text("UPDATE category SET name = 'Unnamed' WHERE name IS NULL"))


    with op.batch_alter_table('category') as batch:
        batch.alter_column('name',
                           existing_type=sa.String(length=50),
                           nullable=False)

def downgrade() -> None:

    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.alter_column('user', 'password',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('user', 'surname',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('user', 'name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_index(op.f('ix_spend_id'), table_name='spend')
    op.alter_column('spend', 'description',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('spend', 'amount',
               existing_type=sa.Float(),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('spend', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_column('spend', 'date')
    op.drop_index(op.f('ix_income_id'), table_name='income')
    op.alter_column('income', 'description',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('income', 'amount',
               existing_type=sa.Float(),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('income', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_column('income', 'date')
    op.add_column('category', sa.Column('category_name', sa.TEXT(), nullable=False))
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_column('category', 'name')

    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('category', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.INTEGER(), nullable=False),
    sa.Column('ownder', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['ownder'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    # ### end Alembic commands ###
