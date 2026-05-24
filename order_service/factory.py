from order_service.client_factory import build_pricing_client
from order_service.service import OrderService
from order_service.store import OrderStore


def build_order_service(store: OrderStore | None = None) -> OrderService:
    """Create OrderService with LOCAL or REMOTE pricing from environment."""
    return OrderService(build_pricing_client(), store=store)
