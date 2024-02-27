from dataclasses import dataclass
from datetime import datetime

import pydantic

from src.domain.contracts.repositories.product_repository import IProductRepository


class InputInventoryProcessorDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime


@dataclass
class InventoryProcessorUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputInventoryProcessorDTO):
        return await self.repository.add_inventory_to(
            input_dto.code, input_dto.supplier, input_dto.expiration_date
        )
