import typing
import uuid

import fastapi as fa
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from apps import models


class Repository(typing.Protocol):
    async def get(self, file_id: str):
        pass

    async def create(
        self, *, file: fa.UploadFile
    ) -> models.File:
        pass


class FileRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    async def get(self, file_id: str):
        resp = await self.session.execute(
            sa.select(models.File).filter_by(id=file_id)
        )
        result = resp.scalar()
        return result

    async def create(
        self, *, file: fa.UploadFile
    ) -> models.File:

        file_id = str(uuid.uuid4())

        if not file.filename:
            file.filename = str(uuid.uuid4())

        url = f'https://localhost:8000/files/download/{file_id}/'
        file_ = models.File(
            file_b=file.file.read(),
            mime_type=file.content_type,
            id=file_id, size=file.file.__sizeof__(),
            name=file.filename, url=url
        )
        self.session.add(file_)
        await self.session.flush()
        await self.session.refresh(file_)
        return file_
