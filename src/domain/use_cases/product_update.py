from dataclasses import dataclass
import pydantic
from datetime import datetime
from typing import Union, Optional
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product


class UpdatableInformation(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    weight_in_kilograms: Optional[float] = None


class InputProductUpdateDTO(pydantic.BaseModel):
    code: str
    supplier: str
    expiration_date: datetime
    update: UpdatableInformation


class OutputProductUpdateDTO(pydantic.BaseModel):
    success: bool
    product: Union[Product, None]
    msg: Union[str, None]


def get_or_default(a, b):
    return a or b


@dataclass
class ProductUpdateUseCase:
    repository: IProductRepository

    async def execute(self, input_dto: InputProductUpdateDTO) -> OutputProductUpdateDTO:
        product = await self.repository.get_by_code_supplier_expiration(
            input_dto.code, input_dto.supplier, input_dto.expiration_date
        )
        if not product:
            return OutputProductUpdateDTO(
                success=False, msg="Product not found", product=None
            )

        any_information_to_update = any(input_dto.update.model_dump().values())
        if (not input_dto.update) or (not any_information_to_update):
            return OutputProductUpdateDTO(
                success=False,
                msg="This request no contains information to update",
                product=None,
            )

        product.title = get_or_default(input_dto.update.title, product.title)
        product.description = get_or_default(
            input_dto.update.description, product.description
        )
        product.buy_price = get_or_default(
            input_dto.update.buy_price, product.buy_price
        )
        product.sell_price = get_or_default(
            input_dto.update.sell_price, product.sell_price
        )
        product.weight_in_kilograms = get_or_default(
            input_dto.update.weight_in_kilograms, product.weight_in_kilograms
        )

        updated_product = await self.repository.update(product)
        if updated_product:
            return OutputProductUpdateDTO(
                success=True, product=updated_product, msg=None
            )

        return OutputProductUpdateDTO(
            success=False, product="update not found", msg=None
        )
