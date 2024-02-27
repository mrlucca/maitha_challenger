from abc import ABC, abstractclassmethod

from src.domain.use_cases.product_inventory_processor import InputInventoryProcessorDTO


class IInventoryRepository(ABC):
    @abstractclassmethod
    async def send(dto: InputInventoryProcessorDTO):
        ...