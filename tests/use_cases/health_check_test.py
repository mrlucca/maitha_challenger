from fastapi.testclient import TestClient
import pytest
from src.domain.use_cases.health_check import HealthCheckUseCase
from src.infra.http.routers.health_check_router import get_health_check_use_case
from src.infra.http.server import setup_and_get_app


@pytest.mark.parametrize(
    "expected_result",
    [
        pytest.param(True, id="available_service"),
        pytest.param(False, id="unavailable_service"),
    ],
)
async def test_heath_check_with(expected_result, health_check_repository_fixture):
    health_check_repository_fixture.is_available.return_value = expected_result
    use_case = HealthCheckUseCase(health_check_repository_fixture)

    result = await use_case.execute()

    assert result.available == expected_result


@pytest.mark.parametrize(
    "expected_result",
    [
        pytest.param(True, id="available_success"),
        pytest.param(False, id="available_fail"),
    ],
)
async def test_heath_check_http_response_with(
    expected_result, health_check_repository_fixture
):
    app = setup_and_get_app()
    health_check_repository_fixture.is_available.return_value = expected_result

    async def mocked_use_case() -> HealthCheckUseCase:
        return HealthCheckUseCase(health_check_repository_fixture)

    app.dependency_overrides[get_health_check_use_case] = mocked_use_case

    client = TestClient(app)
    response = client.get("/api/health/check")
    assert response.status_code == 200
    assert response.json() == {"available": expected_result}
