from abc import ABC, abstractmethod

from src.domain.use_cases.product_inventory_processor import InputInventoryProcessorDTO


class IInventoryRepository(ABC):
    @abstractmethod
    async def send(self, dto: InputInventoryProcessorDTO): ...
