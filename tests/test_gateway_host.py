from decimal import Decimal

from pricing_service.gateway_host import PricingGateway
from pricing_service.models import PricingResult


def test_gateway_host_returns_pricing_result():
    result = PricingGateway.calculate_price("mouse", 1, "regular")
    assert isinstance(result, PricingResult)
    assert result.product_id == "mouse"
    assert result.total_price == Decimal("150.00")
    assert result.discount_percent == Decimal("0")


def test_gateway_host_premium_discount():
    result = PricingGateway.calculate_price("laptop", 1, "premium")
    assert result.discount_percent == Decimal("10")
    assert result.total_price == Decimal("4500.00")
