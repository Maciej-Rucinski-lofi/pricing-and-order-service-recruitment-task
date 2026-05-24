from decimal import Decimal

import pytest

from pricing_service.exceptions import (
    InvalidQuantityError,
    UnknownProductError,
    UnsupportedCustomerTypeError,
)
from pricing_service.rules import PricingRules
from pricing_service.service import PricingService


@pytest.fixture
def pricing() -> PricingService:
    return PricingService()


def test_base_price_regular_no_discount(pricing: PricingService):
    result = pricing.calculate_price("laptop", 1, "regular")
    assert result.unit_price == Decimal("5000")
    assert result.discount_percent == Decimal("0")
    assert result.total_price == Decimal("5000.00")


def test_premium_customer_discount(pricing: PricingService):
    result = pricing.calculate_price("laptop", 1, "premium")
    assert result.discount_percent == Decimal("10")
    assert result.total_price == Decimal("4500.00")


def test_quantity_discount_regular(pricing: PricingService):
    result = pricing.calculate_price("mouse", 10, "regular")
    assert result.discount_percent == Decimal("5")
    assert result.total_price == Decimal("1425.00")


def test_combined_premium_and_quantity_discount(pricing: PricingService):
    result = pricing.calculate_price("laptop", 10, "premium")
    assert result.discount_percent == Decimal("15")
    assert result.total_price == Decimal("42500.00")


def test_discount_cap_at_twenty_percent():
    rules = PricingRules(
        customer_discounts={"whale": Decimal("18")},
        quantity_discounts=[(10, Decimal("5"))],
        max_total_discount_percent=Decimal("20"),
    )
    pricing = PricingService(rules=rules)
    result = pricing.calculate_price("keyboard", 10, "whale")
    assert result.discount_percent == Decimal("20")
    assert result.total_price == Decimal("2400.00")


def test_invalid_product(pricing: PricingService):
    with pytest.raises(UnknownProductError):
        pricing.calculate_price("tablet", 1, "regular")


def test_invalid_quantity_zero(pricing: PricingService):
    with pytest.raises(InvalidQuantityError):
        pricing.calculate_price("laptop", 0, "regular")


def test_invalid_quantity_negative(pricing: PricingService):
    with pytest.raises(InvalidQuantityError):
        pricing.calculate_price("laptop", -1, "regular")


def test_unsupported_customer_type(pricing: PricingService):
    with pytest.raises(UnsupportedCustomerTypeError):
        pricing.calculate_price("laptop", 1, "enterprise")
