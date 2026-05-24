"""Graftcode Gateway entry point — static methods for remote discovery."""

from pricing_service.models import PricingResult
from pricing_service.service import PricingService

_service = PricingService()


class PricingGateway:
    """Hosted pricing API (use this class in Graftcode Gateway / Vision)."""

    @staticmethod
    def calculate_price(
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> PricingResult:
        return _service.calculate_price(product_id, quantity, customer_type)
