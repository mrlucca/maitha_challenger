from src.domain.use_cases.product_create import OutputProductCreateDTO


async def test_execute_product_already_exists(
    product_fake_fixture, product_use_case_fixture
):
    expected_success_result = False
    product_use_case_fixture.repository.exists.return_value = True
    result = await product_use_case_fixture.execute(product_fake_fixture)
    assert result.success == expected_success_result
    assert result.msg == "product already exists"


async def test_execute_create_product_success(
    product_fake_fixture, product_use_case_fixture
):
    expected_success_result = True
    product_use_case_fixture.repository.exists.return_value = False
    product_use_case_fixture.repository.create.return_value = product_fake_fixture
    result = await product_use_case_fixture.execute(product_fake_fixture)
    assert result.success == expected_success_result
    assert result.product == product_fake_fixture


async def test_execute_create_product_error(
    product_fake_fixture, product_use_case_fixture
):
    expected_success_result = False
    product_use_case_fixture.repository.exists.return_value = False
    product_use_case_fixture.repository.create.return_value = None
    result = await product_use_case_fixture.execute(product_fake_fixture)
    assert result.success == expected_success_result
    assert result.msg == "error while get product"
