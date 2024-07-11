import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Zaglushka:
    database_path = os.path.join('DB', 'sqlite', 'user_data.db')
    async_engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}', echo=True)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )