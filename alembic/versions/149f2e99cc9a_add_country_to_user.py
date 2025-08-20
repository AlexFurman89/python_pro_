from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "149f2e99cc9a"
down_revision = "1f7f44e77107"
branch_labels = None
depends_on = None

def upgrade():

    op.add_column(
        "user",
        sa.Column("country", sa.String(length=100), nullable=True)
    )

def downgrade():

    op.drop_column("user", "country")