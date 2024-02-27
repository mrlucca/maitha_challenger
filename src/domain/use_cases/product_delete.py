import pydantic
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class InputProductDeleteDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime


class OutputProductDeleteDTO(pydantic.BaseModel):
    success: bool
    product: Union[Product, None]
    msg: Union[str, None]


@dataclass
class ProductDeleteUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputProductDeleteDTO) -> OutputProductDeleteDTO:
        product = await self.repository.get_by_code_supplier_expiration(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
        )
        if product:
            return OutputProductDeleteDTO(success=True, product=product, msg=None)

        return OutputProductDeleteDTO(
            success=False, msg="Product not found", product=None
        )
