from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    unit_price: Decimal


@dataclass(frozen=True)
class PricingResult:
    product_id: str
    unit_price: Decimal
    quantity: int
    discount_percent: Decimal
    total_price: Decimal
