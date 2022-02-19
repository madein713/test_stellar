import os

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import sessionmaker


DB_NAME = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
PASS = os.getenv('POSTGRES_PASSWORD')
PATH = '/code/apps/static/'

Base = declarative_base()
engine = create_async_engine(
    f"postgresql+asyncpg://{USER}:{PASS}@db/{DB_NAME}", future=True
)
session_factory = sessionmaker(bind=engine, class_=AsyncSession)
