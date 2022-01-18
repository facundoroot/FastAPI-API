"""add foreign key to post table

Revision ID: a2deda022855
Revises: d037edcc6bc1
Create Date: 2022-01-17 21:25:53.084426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2deda022855'
down_revision = 'd037edcc6bc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('user_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
            'posts_users_fk',
            source_table='posts',
            referent_table='users',
            local_cols=['user_id'],
            remote_cols=['id'],
            ondelete='CASCADE'
        )
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
