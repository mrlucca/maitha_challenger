from typing import Self
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from src.domain.use_cases.health_check import HealthCheckUseCase, OutputHealthCheckDTO
from src.infra.postgres.health_check_repository import (
    HealthCheckRepositoryByPostgresWithSqlAlchemy,
)

from src.infra.sqlalchemy.instance import SingletonSqlAlchemyConnection


router = APIRouter(prefix="/api/health")


class SingletonHealthCheckUseCaseFactory:
    _instance = None

    @classmethod
    def factory(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self.db_instance = SingletonSqlAlchemyConnection.get_instance()
        self.repository_instance = HealthCheckRepositoryByPostgresWithSqlAlchemy(
            self.db_instance
        )
        self.use_case_instance = HealthCheckUseCase(self.repository_instance)


async def get_health_check_use_case() -> HealthCheckUseCase:
    return SingletonHealthCheckUseCaseFactory.factory().use_case_instance


@router.get("/check")
async def health_check(
    singleton_use_case: HealthCheckUseCase = Depends(get_health_check_use_case),
) -> OutputHealthCheckDTO:
    return await singleton_use_case.execute()