import pytest
from src.domain.entities.product import Product
from datetime import datetime
from src.domain.contracts.repositories.product_repository import IProductRepository


@pytest.mark.asyncio
async def test_execute_product_found(
    product_delete_use_case_fixture, input_product_delete_dto_fixture
):
    
    now = datetime.now()
    expected_product = Product(
        title="Product",
        description="Description",
        code="ABC123",
        supplier="Supplier",
        inventory_quantity=10,
        buy_price=100.0,
        sell_price=150.0,
        weight_in_kilograms=1.5,
        expiration_date=datetime.now(),
        created_at=now,
        updated_at=now,
    )
    product_delete_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        expected_product
    )
    result = await product_delete_use_case_fixture.execute(
        input_product_delete_dto_fixture
    )
    assert result.success == True
    assert result.product == expected_product
    assert result.msg == None


@pytest.mark.asyncio
async def test_execute_product_not_found(
    product_delete_use_case_fixture, input_product_delete_dto_fixture
):
    product_delete_use_case_fixture.repository.get_by_code_supplier_expiration.return_value = (
        None
    )
    result = await product_delete_use_case_fixture.execute(
        input_product_delete_dto_fixture
    )
    assert result.success == False
    assert result.product == None
    assert result.msg == "Product not found"
