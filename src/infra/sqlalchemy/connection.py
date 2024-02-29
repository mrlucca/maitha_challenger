from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


def _build_postgres_url_from_environments():
    postgres_host = config("POSTGRES_HOST")
    postgres_user = config("POSTGRES_USER")
    postgres_password = config("POSTGRES_PASSWORD")
    postgres_db = config("POSTGRES_DB")

    return f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"


class SingletonSqlAlchemyConnection:
    _instance = None

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.url = _build_postgres_url_from_environments()
        self.engine = create_async_engine(self.url, echo=True, future=True)
        self.async_session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )
