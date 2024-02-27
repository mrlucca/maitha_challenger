from dataclasses import dataclass
from datetime import datetime
from typing import Self

import pydantic


class Product(pydantic.BaseModel):
    title: str
    description: str
    code: str
    supplier: str
    inventory_quantity: int
    buy_price: float
    sell_price: float
    weight_in_kilograms: float
    expiration_date: datetime
    created_at: datetime = None
    updated_at: datetime = None

    @staticmethod
    def from_input_dto(dto) -> Self:
        return Product(
            title=dto.title,
            description=dto.description,
            code=dto.code,
            supplier=dto.supplier,
            inventory_quantity=dto.inventory_quantity,
            buy_price=dto.buy_price,
            sell_price=dto.sell_price,
            weight_in_kilograms=dto.weight_in_kilograms,
            expiration_date=dto.expiration_date,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
