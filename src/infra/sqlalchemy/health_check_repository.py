from src.domain.contracts.repositories.health_check_repository import (
    IHealthCheckRepository,
)
from sqlalchemy import exc, text

from src.infra.sqlalchemy.instance import SingletonSqlAlchemyConnection


class SqlAlchemyHealthCheckRepository(IHealthCheckRepository):
    def __init__(self, sqlalchemy_instance: SingletonSqlAlchemyConnection):
        self.sqlalchemy_instance = sqlalchemy_instance

    async def is_available(self):
        async with self.sqlalchemy_instance.async_session() as session:
            try:
                async with session.begin():
                    await session.execute(text("SELECT 1"))
                return True
            except exc.SQLAlchemyError as e:
                return False
