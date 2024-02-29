import pytest
from datetime import datetime

from src.infra.sqlalchemy.models import make_product_id_from_base


@pytest.mark.asyncio
async def test_execute_product_found(
    product_delete_use_case_fixture, input_product_delete_dto_fixture
):

    expected_product_product_id = make_product_id_from_base("test", "test", datetime.now())
    product_delete_use_case_fixture.repository.exists_from.return_value = True
    product_delete_use_case_fixture.repository.remove.return_value = (
        expected_product_product_id
    )
    result = await product_delete_use_case_fixture.execute(
        input_product_delete_dto_fixture
    )
    assert result.success is True
    assert result.product_id == expected_product_product_id
    assert result.msg is None


@pytest.mark.asyncio
async def test_execute_product_not_found(
    product_delete_use_case_fixture, input_product_delete_dto_fixture
):
    expected_product_product_id = make_product_id_from_base("test", "test", datetime.now())
    product_delete_use_case_fixture.repository.exists_from.return_value = False
    product_delete_use_case_fixture.repository.remove.return_value = (
        expected_product_product_id
    )
    result = await product_delete_use_case_fixture.execute(
        input_product_delete_dto_fixture
    )
    assert result.success is False
    assert result.product_id is None
    assert result.msg == "Product not exists"


@pytest.mark.asyncio
async def test_execute_product_not_found(
    product_delete_use_case_fixture, input_product_delete_dto_fixture
):
    expected_product_product_id = None
    product_delete_use_case_fixture.repository.exists_from.return_value = True
    product_delete_use_case_fixture.repository.remove.return_value = expected_product_product_id
    result = await product_delete_use_case_fixture.execute(
        input_product_delete_dto_fixture
    )
    assert result.success is False
    assert result.product_id is expected_product_product_id
    assert result.msg == "product not deleted"
