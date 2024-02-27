from abc import ABC, abstractmethod
import datetime
from typing import List

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def create(product: Product) -> Product: ...

    @abstractmethod
    async def exists(product: Product) -> bool: ...

    @abstractmethod
    async def add_inventory_from_code(code: str) -> Product: ...

    @abstractmethod
    async def get_inventory_from_code(code: str) -> Product: ...

    @abstractmethod
    async def from_code(code: str) -> Product: ...

    @abstractmethod
    async def from_supplier(supplier: str) -> List[Product]: ...

    @abstractmethod
    async def expiration_date(date: datetime): ...
