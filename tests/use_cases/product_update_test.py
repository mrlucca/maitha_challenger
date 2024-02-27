from src.domain.entities.product import Product
from src.domain.contracts.repositories.product_repository import IProductRepository
from unittest.mock import MagicMock, AsyncMock

from src.domain.use_cases.product_update import (
    InputProductUpdateDTO,
    UpdatableInformation,
)


async def test_execute_product_not_found(product_update_use_case_fixture):
    product_update_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        None
    )
    input_dto = InputProductUpdateDTO(
        code="123",
        supplier="Supplier",
        expiration_date="2024-12-31T23:59:59",
        update=UpdatableInformation(
            title=None,
            buy_price=None,
            weight_in_kilograms=None,
            description=None,
            sell_price=None,
        ),
    )

    result = await product_update_use_case_fixture.execute(input_dto)
    assert result.success == False
    assert result.msg == "Product not found"
    assert result.product == None


async def test_execute_no_information_to_update(
    product_update_use_case_fixture, product_fake_fixture
):
    input_dto = InputProductUpdateDTO(
        code="123",
        supplier="Supplier",
        expiration_date="2024-12-31T23:59:59",
        update=UpdatableInformation(
            title=None,
            buy_price=None,
            weight_in_kilograms=None,
            description=None,
            sell_price=None,
        ),
    )
    product_update_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        product_fake_fixture
    )

    result = await product_update_use_case_fixture.execute(input_dto)
    assert result.success == False
    assert result.msg == "This request no contains information to update"


async def test_execute_update_successfully(
    product_update_use_case_fixture, product_fake_fixture
):
    product_update_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        product_fake_fixture
    )
    product_update_use_case_fixture.repository.update.return_value = (
        product_fake_fixture
    )
    input_dto = InputProductUpdateDTO(
        code="123",
        supplier="Supplier",
        expiration_date="2024-12-31T23:59:59",
        update=UpdatableInformation(
            title="New Title",
            buy_price=15.0,
            weight_in_kilograms=2.0,
            description=None,
            sell_price=None,
        ),
    )

    result = await product_update_use_case_fixture.execute(input_dto)
    assert result.success == True
    assert result.msg == None
    assert result.product.title == "New Title"
    assert result.product.buy_price == 15.0
    assert result.product.weight_in_kilograms == 2.0
