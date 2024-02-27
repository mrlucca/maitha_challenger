import pydantic

from dataclasses import dataclass
from src.domain.contracts.repositories.health_check_repository import (
    IHealthCheckRepository,
)


class OutputHealthCheckDTO(pydantic.BaseModel):
    available: bool


@dataclass(slots=True)
class HealthCheckUseCase:
    health_check_repository: IHealthCheckRepository

    async def execute(self) -> OutputHealthCheckDTO:
        service_is_available = await self.health_check_repository.is_available()
        return OutputHealthCheckDTO(available=service_is_available)
