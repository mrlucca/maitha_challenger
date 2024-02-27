from dataclasses import dataclass
from datetime import datetime
from typing import Union
import pydantic

from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class InputProductCreateDTO(pydantic.BaseModel):
    title: str
    description: str
    code: str
    supplier: str
    inventory_quantity: int
    buy_price: float
    sell_price: float
    weight_in_kilograms: float
    expiration_date: datetime


class OutputProductCreateDTO(pydantic.BaseModel):
    success: bool
    product: Union[Product, None]
    msg: Union[str, None]


@dataclass(slots=True)
class ProductCreateUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputProductCreateDTO) -> OutputProductCreateDTO:
        raw_product = Product.from_input_dto(input_dto)
        if await self.repository.exists(raw_product):
            return OutputProductCreateDTO(
                success=False, product=None, msg="product already exists"
            )

        response = await self.repository.create(raw_product)
        if response is not None:
            return OutputProductCreateDTO(success=True, product=response, msg=None)

        return OutputProductCreateDTO(
            success=False, msg="error while get product", product=None
        )
