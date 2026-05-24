from decimal import Decimal

from pricing_service.catalog import load_products
from pricing_service.rules import load_rules


def test_products_config_loads():
    products = load_products()
    assert set(products) == {"laptop", "mouse", "keyboard"}
    assert products["laptop"].unit_price == Decimal("5000")


def test_pricing_rules_config_loads():
    rules = load_rules()
    assert rules.customer_discounts["premium"] == Decimal("10")
    assert rules.max_total_discount_percent == Decimal("20")
