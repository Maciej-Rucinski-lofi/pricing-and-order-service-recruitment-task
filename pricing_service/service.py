from pathlib import Path

from pricing_service.catalog import load_products
from pricing_service.models import PricingResult, Product
from pricing_service.rules import PricingRules, load_rules


class PricingService:
    """Public API exposed through Graftcode Gateway in later phases."""

    def __init__(
        self,
        products: dict[str, Product] | None = None,
        rules: PricingRules | None = None,
        products_path: Path | None = None,
        rules_path: Path | None = None,
    ) -> None:
        self._products = products if products is not None else load_products(products_path)
        self._rules = rules if rules is not None else load_rules(rules_path)

    def calculate_price(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> PricingResult:
        """Calculate price with discounts. Implemented in Phase 3."""
        raise NotImplementedError("Price calculation is implemented in Phase 3.")
