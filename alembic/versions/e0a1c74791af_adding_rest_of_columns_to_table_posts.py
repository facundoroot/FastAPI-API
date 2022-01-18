"""adding rest of columns to table posts

Revision ID: e0a1c74791af
Revises: a2deda022855
Create Date: 2022-01-17 21:43:32.903721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a1c74791af'
down_revision = 'a2deda022855'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )
    pass


def downgrade():
    op.drop_table('posts', 'published')
    op.drop_table('posts', 'created_at')
    pass
