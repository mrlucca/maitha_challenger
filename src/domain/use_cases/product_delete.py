import pydantic
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Optional

from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class InputProductDeleteDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime


class OutputProductDeleteDTO(pydantic.BaseModel):
    success: bool
    product_id: Optional[str] = None
    msg: Optional[str] = None

    @classmethod
    def do_success(cls, product_id: str):
        return cls(success=True, product_id=product_id)

    @classmethod
    def do_error(cls, msg: str):
        return cls(success=False, msg=msg)


@dataclass
class ProductDeleteUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputProductDeleteDTO) -> OutputProductDeleteDTO:
        product_exists = await self.repository.exists_from(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
        )
        if not product_exists:
            return OutputProductDeleteDTO.do_error("Product not exists")

        product_id = await self.repository.remove(
            code=input_dto.code,
            supplier=input_dto.supplier,
            expiration_date=input_dto.expiration_date,
        )

        if not product_id:
            return OutputProductDeleteDTO.do_error(
                "product not deleted",
            )

        return OutputProductDeleteDTO.do_success(product_id)
