from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CustomerType(Enum):
    CPF = "CP"
    CNPJ = "CN"


class PaymentMethod(Enum):
    CREDIT_CARD = "CD"
    DEBIT_CARD = "DC"
    CASH = "CA"


@dataclass(slots=True)
class Purchase:
    id: int
    product_id: str
    quantity: int
    purchase_date: datetime
    identification: str
    identification_type: CustomerType
    payment_method: PaymentMethod
    total_amount: float
