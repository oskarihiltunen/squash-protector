from sqlalchemy_defaults import Column

from squash.extensions import db
from .project import Project


class CommitStatus(db.Model):
    __tablename__ = 'commit_status'

    commit_sha = Column(
        db.Unicode(40),
        primary_key=True,
        index=True,
        unique=True,
    )
    project_id = Column(
        None,
        db.ForeignKey(Project.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
        index=True,
        unique=False,
    )
    status = Column(
        db.Enum(
            'pending',
            'success',
            'failure',
            native_enum=False,
        )
    )

    project = db.relationship(Project)
