import importlib
from decimal import Decimal

import pytest


@pytest.fixture
def order_gateway_module(monkeypatch):
    monkeypatch.setenv("PRICING_MODE", "LOCAL")
    import order_service.gateway_host as gateway_host

    return importlib.reload(gateway_host)


def test_order_gateway_place_order(order_gateway_module):
    result = order_gateway_module.OrderGateway.place_order("laptop", 1, "regular")
    assert result.status == "created"
    assert result.total_price == Decimal("5000.00")


def test_order_gateway_get_order(order_gateway_module):
    placed = order_gateway_module.OrderGateway.place_order("mouse", 2, "regular")
    fetched = order_gateway_module.OrderGateway.get_order(placed.order_id)
    assert fetched == placed
