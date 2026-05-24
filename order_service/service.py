from order_service.models import OrderResult
from order_service.pricing_port import PricingClient
from order_service.store import OrderStore


class OrderService:
    """Public API exposed through Graftcode Vision in later phases."""

    def __init__(
        self,
        pricing_client: PricingClient,
        store: OrderStore | None = None,
    ) -> None:
        self._pricing = pricing_client
        self._store = store or OrderStore()

    def place_order(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> OrderResult:
        """Place an order. Implemented in Phase 5."""
        raise NotImplementedError(
            "Order placement is implemented in Phase 5 "
            f"({product_id=}, {quantity=}, {customer_type=})."
        )

    def get_order(self, order_id: str) -> OrderResult | None:
        return self._store.get(order_id)
