"""Graftcode Gateway entry point for Order Service."""

from order_service.models import OrderResult

# Lazy init: gg's module analyzer breaks on stdlib logging when factory loads at import time.
_service = None


def _get_service():
    global _service
    if _service is None:
        from order_service.factory import build_order_service

        _service = build_order_service()
    return _service


class OrderGateway:
    """Hosted order API (use this class in Graftcode Gateway / Vision)."""

    @staticmethod
    def place_order(
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> OrderResult:
        return _get_service().place_order(product_id, quantity, customer_type)

    @staticmethod
    def get_order(order_id: str) -> OrderResult | None:
        return _get_service().get_order(order_id)
