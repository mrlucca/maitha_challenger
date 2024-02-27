from dataclasses import dataclass
from typing import Union
import pydantic

from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class OutputProductCreateDTO(pydantic.BaseModel):
    success: bool
    product: Union[Product, None]
    msg: Union[str, None]


@dataclass(slots=True)
class ProductUseCase:
    repository: IProductRepository

    async def execute(self, product: Product) -> OutputProductCreateDTO:
        if await self.repository.exists(product):
            return OutputProductCreateDTO(
                success=False, product=None, msg="product already exists"
            )

        response = await self.repository.create(product)
        if response is not None:
            return OutputProductCreateDTO(success=True, product=response, msg=None)

        return OutputProductCreateDTO(
            success=False, msg="error while get product", product=None
        )
