import logging
import time
from decimal import Decimal

from pricing_service.exceptions import PricingError
from pricing_service.models import PricingResult

from order_service.exceptions import PricingUnavailableError
from order_service.graft_loader import load_pricing_gateway_class

logger = logging.getLogger(__name__)

_MAX_ATTEMPTS = 3
_RETRY_DELAY_SEC = 0.5


def _to_pricing_result(raw: object) -> PricingResult:
    if isinstance(raw, PricingResult):
        return raw
    if isinstance(raw, dict):
        return PricingResult(
            product_id=str(raw["product_id"]),
            unit_price=Decimal(str(raw["unit_price"])),
            quantity=int(raw["quantity"]),
            discount_percent=Decimal(str(raw["discount_percent"])),
            total_price=Decimal(str(raw["total_price"])),
        )
    return PricingResult(
        product_id=str(getattr(raw, "product_id")),
        unit_price=Decimal(str(getattr(raw, "unit_price"))),
        quantity=int(getattr(raw, "quantity")),
        discount_percent=Decimal(str(getattr(raw, "discount_percent"))),
        total_price=Decimal(str(getattr(raw, "total_price"))),
    )


class RemotePricingClient:
    """REMOTE mode — calls Pricing Service via generated Graft."""

    def __init__(self, pricing_gateway: type | None = None) -> None:
        self._pricing_gateway = pricing_gateway

    def _get_gateway(self) -> type:
        if self._pricing_gateway is None:
            self._pricing_gateway = load_pricing_gateway_class()
        return self._pricing_gateway

    def calculate_price(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ) -> PricingResult:
        gateway = self._get_gateway()
        last_error: Exception | None = None

        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                raw = gateway.calculate_price(product_id, quantity, customer_type)
                return _to_pricing_result(raw)
            except PricingError:
                raise
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Pricing Graft call failed (attempt %s/%s): product_id=%s error=%s",
                    attempt,
                    _MAX_ATTEMPTS,
                    product_id,
                    exc,
                )
                if attempt < _MAX_ATTEMPTS:
                    time.sleep(_RETRY_DELAY_SEC)

        raise PricingUnavailableError(
            "Pricing service is unavailable via Graft",
            cause=last_error,
        ) from last_error
