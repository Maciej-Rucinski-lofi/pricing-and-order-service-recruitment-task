from order_service.models import OrderResult


class OrderStore:
    """In-memory order storage (no database required)."""

    def __init__(self) -> None:
        self._orders: dict[str, OrderResult] = {}

    def save(self, order: OrderResult) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> OrderResult | None:
        return self._orders.get(order_id)

    def list_all(self) -> list[OrderResult]:
        return list(self._orders.values())
