"""Initial version."""

# revision identifiers, used by Alembic.
revision = '43ab9a6a64d7'
down_revision = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'project',
        sa.Column('id', UUIDType(binary=False), nullable=False),
        sa.Column('repo', sa.UnicodeText(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('repo')
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=True)
    op.create_table(
        'commit_status',
        sa.Column('commit_sha', sa.Unicode(length=40), nullable=False),
        sa.Column('project_id', UUIDType(binary=False), nullable=False),
        sa.Column(
            'status',
            sa.Enum(u'pending', u'success', u'failure', native_enum=False),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['project_id'],
            [u'project.id'],
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('commit_sha', 'project_id')
    )
    op.create_index(
        op.f('ix_commit_status_commit_sha'),
        'commit_status',
        ['commit_sha'],
        unique=True,
    )
    op.create_index(
        op.f('ix_commit_status_project_id'),
        'commit_status',
        ['project_id'],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f('ix_commit_status_project_id'),
        table_name='commit_status',
    )
    op.drop_index(
        op.f('ix_commit_status_commit_sha'),
        table_name='commit_status',
    )
    op.drop_table('commit_status')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')

