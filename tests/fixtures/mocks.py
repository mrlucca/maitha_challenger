import datetime
from unittest.mock import AsyncMock
import pytest

from src.domain.contracts.repositories.health_check_repository import (
    IHealthCheckRepository,
)
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product
from src.domain.use_cases.product_create import ProductUseCase


@pytest.fixture
def health_check_repository_fixture():
    return AsyncMock(spec=IHealthCheckRepository)


@pytest.fixture
def product_use_case_fixture():
    repository_mock = AsyncMock(spec=IProductRepository)
    return ProductUseCase(repository_mock)


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
