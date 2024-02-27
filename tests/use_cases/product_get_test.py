from datetime import datetime
from src.domain.use_cases.product_get import InputProductGetDTO


async def test_execute_product_found(
    product_get_use_case_fixture, product_fake_fixture
):

    input_dto = InputProductGetDTO(
        code="123",
        supplier="Test Supplier",
        expiration_date=datetime.now(),
    )
    product_get_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        product_fake_fixture
    )
    result = await product_get_use_case_fixture.execute(input_dto)
    assert result.success is True
    assert result.product == product_fake_fixture
    assert result.msg is None


async def test_execute_product_not_found(product_get_use_case_fixture):
    input_dto = InputProductGetDTO(
        code="123",
        supplier="Test Supplier",
        expiration_date=datetime.now(),
    )
    product_get_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        None
    )
    result = await product_get_use_case_fixture.execute(input_dto)
    assert result.success is False
    assert result.product is None
    assert result.msg == "product does not exists"
