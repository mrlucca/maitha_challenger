from unittest.mock import AsyncMock
import pytest

from src.domain.contracts.repositories.health_check_repository import (
    IHealthCheckRepository,
)


@pytest.fixture
def health_check_repository_fixture():
    return AsyncMock(spec=IHealthCheckRepository)
