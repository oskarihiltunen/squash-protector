from sqlalchemy_defaults import Column
from sqlalchemy_utils import UUIDType

from squash.extensions import db


class Project(db.Model):
    __tablename__ = 'project'

    id = Column(
        UUIDType(binary=False),
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
    )
    repo = Column(
        db.UnicodeText,
        unique=True,
    )
    access_token = Column(
        db.UnicodeText,
    )
