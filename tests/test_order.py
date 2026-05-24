from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from order_service.exceptions import PricingUnavailableError
from order_service.factory import build_order_service
from order_service.service import OrderService
from order_service.store import OrderStore
from pricing_service.exceptions import UnknownProductError
from pricing_service.models import PricingResult


def _pricing_result(total: str = "100.00") -> PricingResult:
    return PricingResult(
        product_id="mouse",
        unit_price=Decimal("100"),
        quantity=1,
        discount_percent=Decimal("0"),
        total_price=Decimal(total),
    )


def test_place_order_happy_path():
    store = OrderStore()
    pricing = MagicMock()
    pricing.calculate_price.return_value = _pricing_result("150.00")

    service = OrderService(pricing, store=store)
    order = service.place_order("mouse", 1, "regular")

    assert order.status == "created"
    assert order.product_id == "mouse"
    assert order.total_price == Decimal("150.00")
    assert store.get(order.order_id) == order
    pricing.calculate_price.assert_called_once_with("mouse", 1, "regular")


def test_place_order_pricing_validation_does_not_persist():
    store = OrderStore()
    pricing = MagicMock()
    pricing.calculate_price.side_effect = UnknownProductError("tablet")

    service = OrderService(pricing, store=store)
    with pytest.raises(UnknownProductError):
        service.place_order("tablet", 1, "regular")

    assert store.list_all() == []


def test_place_order_pricing_unavailable_does_not_persist():
    store = OrderStore()
    pricing = MagicMock()
    pricing.calculate_price.side_effect = PricingUnavailableError("down")

    service = OrderService(pricing, store=store)
    with pytest.raises(PricingUnavailableError):
        service.place_order("mouse", 1, "regular")

    assert store.list_all() == []


def test_place_order_local_integration(monkeypatch):
    monkeypatch.setenv("PRICING_MODE", "LOCAL")
    service = build_order_service()
    order = service.place_order("laptop", 1, "regular")
    assert order.total_price == Decimal("5000.00")
    assert service.get_order(order.order_id) is not None
