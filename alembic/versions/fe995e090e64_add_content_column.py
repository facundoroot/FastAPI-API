"""add content column

Revision ID: fe995e090e64
Revises: 75c502acec98
Create Date: 2022-01-17 20:07:09.761310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe995e090e64'
down_revision = '75c502acec98'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column(
        'posts',
        'content'
    )
    pass
