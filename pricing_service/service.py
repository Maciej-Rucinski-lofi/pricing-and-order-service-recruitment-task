from decimal import Decimal
from pathlib import Path

from pricing_service.catalog import get_product, load_products
from pricing_service.constants import round_money
from pricing_service.exceptions import (
    InvalidQuantityError,
    UnknownProductError,
)
from pricing_service.models import PricingResult, Product
from pricing_service.rules import PricingRules, calculate_discount_percent, load_rules


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
        if quantity < 1:
            raise InvalidQuantityError(quantity)

        product = get_product(self._products, product_id)
        if product is None:
            raise UnknownProductError(product_id)

        discount_percent = calculate_discount_percent(
            self._rules, quantity, customer_type
        )
        subtotal = product.unit_price * quantity
        multiplier = (Decimal("100") - discount_percent) / Decimal("100")
        total_price = round_money(subtotal * multiplier)

        return PricingResult(
            product_id=product_id,
            unit_price=product.unit_price,
            quantity=quantity,
            discount_percent=discount_percent,
            total_price=total_price,
        )
