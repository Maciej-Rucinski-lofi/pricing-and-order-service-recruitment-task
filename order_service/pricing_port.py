from typing import Protocol

from pricing_service.models import PricingResult


class PricingClient(Protocol):
    def calculate_price(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> PricingResult: ...
