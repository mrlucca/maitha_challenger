from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


class SingletonSqlAlchemyConnection:
    _instance = None

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.url = self.build_url()
        self.engine = create_async_engine(self.url, echo=True, future=True)
        self.async_session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

    def build_url(self):
        postgres_host = config("POSTGRES_HOST")
        postgres_user = config("POSTGRES_USER")
        postgres_password = config("POSTGRES_PASSWORD")
        postgres_db = config("POSTGRES_DB")

        if None in [postgres_host, postgres_user, postgres_password, postgres_db]:
            raise EnvironmentError(
                "Variáveis de ambiente do banco de dados não estão configuradas corretamente"
            )

        return f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
