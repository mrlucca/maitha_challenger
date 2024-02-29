from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pydantic

from src.domain.contracts.repositories.inventory_repository import IInventoryRepository
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.use_cases.product_inventory_processor import (
    InputInventoryProcessorDTO,
    InventoryAction,
)


class InputProductSendInventoryDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime
    action: InventoryAction


class OutputProductSendInventoryDTO(pydantic.BaseModel):
    success: bool
    message: Optional[str] = None


@dataclass
class ProductSendInventoryUseCase:
    repository: IInventoryRepository
    product_repository: IProductRepository

    async def execute(
        self, input_dto: InputProductSendInventoryDTO
    ) -> OutputProductSendInventoryDTO:
        product_exists = await self.product_repository.exists_from(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
        )
        if not product_exists:
            return OutputProductSendInventoryDTO(
                success=False, message="product not exists"
            )

        input_inventory_processor_dto = InputInventoryProcessorDTO(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
            action=input_dto.action,
        )
        await self.repository.send(input_inventory_processor_dto)
        return OutputProductSendInventoryDTO(
                success=True, message="sent event"
            )
