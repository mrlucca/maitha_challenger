from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import pydantic

from src.domain.contracts.repositories.product_repository import IProductRepository


class InventoryAction(Enum):
    ADD = "a"
    REMOVE = "r"


class InputInventoryProcessorDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime
    action: InventoryAction


@dataclass
class InventoryProcessorUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputInventoryProcessorDTO):
        match input_dto.action:
            case InventoryAction.ADD:
                await self.repository.add_inventory_to(
                    input_dto.code, input_dto.supplier, input_dto.expiration_date
                )

            case InventoryAction.REMOVE:
                await self.repository.remove_inventory_from(
                    input_dto.code, input_dto.supplier, input_dto.expiration_date
                )
