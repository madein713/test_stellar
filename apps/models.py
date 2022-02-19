from datetime import datetime

import sqlalchemy as sa

from apps import Base


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.String(38), primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now)


class File(BaseModel):
    __tablename__ = 'files'

    file_b = sa.Column(sa.LargeBinary)
    mime_type = sa.Column(sa.String(20))
    size = sa.Column(sa.Integer())
    name = sa.Column(sa.String(255))
    url = sa.Column(sa.String(100))
