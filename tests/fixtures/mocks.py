import datetime
from unittest.mock import AsyncMock
import pytest

from src.domain.contracts.repositories.health_check_repository import (
    IHealthCheckRepository,
)
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product
from src.domain.use_cases.product_create import ProductCreateUseCase
from src.domain.use_cases.product_delete import (
    InputProductDeleteDTO,
    ProductDeleteUseCase,
)
from src.domain.use_cases.product_get import ProductGetUseCase
from src.domain.use_cases.product_update import ProductUpdateUseCase


@pytest.fixture
def health_check_repository_fixture():
    return AsyncMock(spec=IHealthCheckRepository)


@pytest.fixture
def product_repository_fixture():
    return AsyncMock(spec=IProductRepository)


@pytest.fixture
def product_use_case_fixture(product_repository_fixture):
    return ProductCreateUseCase(product_repository_fixture)


@pytest.fixture
def product_delete_use_case_fixture(product_repository_fixture):
    return ProductDeleteUseCase(repository=product_repository_fixture)


@pytest.fixture
def product_update_use_case_fixture(product_repository_fixture):
    return ProductUpdateUseCase(repository=product_repository_fixture)


@pytest.fixture
def product_get_use_case_fixture(product_repository_fixture):
    return ProductGetUseCase(product_repository_fixture)


@pytest.fixture
def input_product_delete_dto_fixture():
    return InputProductDeleteDTO(
        code="ABC123",
        supplier="Supplier",
        expiration_date=datetime.datetime.now(datetime.UTC),
    )


@pytest.fixture
def product_fake_fixture():
    return Product(
        title="Test Product",
        description="Test Description",
        code="ABC123",
        supplier="Supplier",
        inventory_quantity=10,
        buy_price=10.50,
        sell_price=20.00,
        weight_in_kilograms=1.5,
        expiration_date="2024-12-31",
        created_at=datetime.datetime.now(datetime.UTC),
        updated_at=datetime.datetime.now(datetime.UTC),
    )
