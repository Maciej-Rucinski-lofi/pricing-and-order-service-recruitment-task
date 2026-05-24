from order_service.exceptions import PricingUnavailableError
from order_service.pricing_port import PricingClient


class RemotePricingClient:
    """REMOTE mode — calls Pricing Service via generated Graft (Phase 4+)."""

    def __init__(self) -> None:
        pass

    def calculate_price(
        self,
        product_id: str,
        quantity: int,
        customer_type: str,
    ):
        raise PricingUnavailableError("Not configured — set GRAFT_CONFIG and install Pricing Graft.")
