from pricing_service.service import PricingService


class LocalPricingClient:
    """In-process pricing (modular monolith / LOCAL mode)."""

    def __init__(self, pricing_service: PricingService | None = None) -> None:
        self._pricing = pricing_service or PricingService()

    def calculate_price(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ):
        return self._pricing.calculate_price(product_id, quantity, customer_type)
