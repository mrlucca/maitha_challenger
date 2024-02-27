from src.domain.use_cases.health_check import HealthCheckUseCase



async def test_heath_check_with_unavailable_service(health_check_repository_fixture):
    expected_result = True
    health_check_repository_fixture.is_available.return_value = expected_result
    use_case = HealthCheckUseCase(health_check_repository_fixture)

    result = await use_case.execute()

    assert result.available == expected_result


async def test_heath_check_with_available_service(health_check_repository_fixture):
    expected_result = False
    health_check_repository_fixture.is_available.return_value = expected_result
    use_case = HealthCheckUseCase(health_check_repository_fixture)

    result = await use_case.execute()

    assert result.available == expected_result