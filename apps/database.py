import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from apps import Base, engine
from apps import session_factory


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    session: Session = session_factory()
    try:
        yield session
    finally:
        try:
            await session.commit()
        except sa.exc.IntegrityError:
            await session.rollback()
        finally:
            await session.close()
