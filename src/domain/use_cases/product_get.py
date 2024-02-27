from dataclasses import dataclass
from datetime import datetime
from typing import Union
import pydantic
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class InputProductGetDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime


class OutputProductGetDTO(pydantic.BaseModel):
    success: bool
    product: Union[Product, None]
    msg: Union[str, None]


@dataclass
class ProductGetUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputProductGetDTO) -> OutputProductGetDTO:
        product = await self.repository.get_by_code_supplier_expiration(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
        )

        if not product:
            return OutputProductGetDTO(
                success=False, msg="product does not exists", product=None
            )

        return OutputProductGetDTO(success=True, product=product, msg=None)
