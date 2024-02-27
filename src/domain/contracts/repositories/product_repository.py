from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def create(product: Product) -> Product | None: ...

    @abstractmethod
    async def exists(product: Product) -> bool: ...

    @abstractmethod
    async def update(product: Product) -> Product | None: ...

    @abstractmethod
    async def add_inventory_to(
        code: str, supplier: str, expiration_date: datetime
    ) -> Product: ...

    @abstractmethod
    async def remove_inventory_from(
        code: str, supplier: str, expiration_date: datetime
    ) -> Product: ...

    @abstractmethod
    async def get_by_code_supplier_expiration(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Optional[Product]: ...
