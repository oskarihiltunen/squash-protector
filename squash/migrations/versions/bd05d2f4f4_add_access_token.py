"""Add access token"""

# revision identifiers, used by Alembic.
revision = 'bd05d2f4f4'
down_revision = '43ab9a6a64d7'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        'project',
        sa.Column('access_token', sa.UnicodeText(), nullable=False),
    )


def downgrade():
    op.drop_column('project', 'access_token')
