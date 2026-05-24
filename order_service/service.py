import logging
import uuid

from pricing_service.exceptions import PricingError
from pricing_service.models import PricingResult

from order_service.exceptions import PricingUnavailableError
from order_service.models import OrderResult
from order_service.pricing_port import PricingClient
from order_service.store import OrderStore

logger = logging.getLogger(__name__)


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
        try:
            pricing = self._pricing.calculate_price(
                product_id, quantity, customer_type
            )
        except PricingError:
            logger.warning(
                "Order rejected (pricing validation): product_id=%s quantity=%s customer_type=%s",
                product_id,
                quantity,
                customer_type,
            )
            raise
        except PricingUnavailableError:
            logger.error(
                "Order failed (pricing unavailable): product_id=%s quantity=%s",
                product_id,
                quantity,
            )
            raise
        except Exception as exc:
            logger.exception(
                "Order failed (unexpected pricing error): product_id=%s",
                product_id,
            )
            raise PricingUnavailableError(
                "Pricing service error",
                cause=exc,
            ) from exc

        order = _build_order(product_id, quantity, customer_type, pricing)
        self._store.save(order)
        logger.info(
            "Order created: order_id=%s product_id=%s total_price=%s",
            order.order_id,
            order.product_id,
            order.total_price,
        )
        return order

    def get_order(self, order_id: str) -> OrderResult | None:
        return self._store.get(order_id)

    def list_orders(self) -> list[OrderResult]:
        return self._store.list_all()


def _build_order(
    product_id: str,
    quantity: int,
    customer_type: str,
    pricing: PricingResult,
) -> OrderResult:
    return OrderResult(
        order_id=str(uuid.uuid4()),
        product_id=product_id,
        quantity=quantity,
        customer_type=customer_type,
        total_price=pricing.total_price,
        status="created",
    )
