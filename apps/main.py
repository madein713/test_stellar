import json

import fastapi as fa
from sqlalchemy.orm.session import Session

from apps import database
from apps.repository import FileRepository


app = fa.FastAPI()


@app.on_event("startup")
async def startup():
    await database.create_db()


@app.get("/files/info/{file_id}")
async def get_file(
    file_id: str, session: Session = fa.Depends(database.get_session)
) -> fa.Response:
    repo = FileRepository(session=session)
    file = await repo.get(file_id=file_id)

    if not file:
        raise fa.HTTPException(status_code=404, detail='File not found')

    return fa.Response(
        json.dumps(
            {
                'file_id': file.id,
                'url': file.url,
                'mime_type': file.mime_type,
                'size': file.size,
                'upload_date': file.created_at.isoformat(),
                'filename': file.name
            }
        )
    )


@app.post("/files/upload")
async def upload(
    file: fa.UploadFile,
    session: Session = fa.Depends(database.get_session)
) -> fa.Response:
    file_repo = FileRepository(session=session)

    file = await file_repo.create(file=file)

    return fa.Response(
        json.dumps(
            {
                'file_id': file.id,
                'url': file.url
            }
        )
    )


@app.get('/files/download/{file_id}')
async def download_file(
    file_id: str,
    session: Session = fa.Depends(database.get_session)
) -> fa.Response:
    repo = FileRepository(session=session)
    file = await repo.get(file_id=file_id)

    if not file:
        raise fa.HTTPException(status_code=404, detail='File not found')

    return fa.Response(
        file.file_b,
        media_type=file.mime_type
    )
