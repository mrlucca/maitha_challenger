from dataclasses import dataclass
from datetime import datetime

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
    created_at: datetime
    updated_at: datetime
