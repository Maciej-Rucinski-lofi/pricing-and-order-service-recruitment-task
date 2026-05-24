import os

from order_service.pricing_local import LocalPricingClient
from order_service.pricing_port import PricingClient
from order_service.pricing_remote import RemotePricingClient


def build_pricing_client() -> PricingClient:
    """Select LOCAL or REMOTE pricing backend from environment (PRICING_MODE)."""
    mode = os.getenv("PRICING_MODE", "LOCAL").strip().upper()
    if mode == "LOCAL":
        return LocalPricingClient()
    if mode == "REMOTE":
        return RemotePricingClient()
    raise ValueError(f"Unsupported PRICING_MODE: {mode!r}. Use LOCAL or REMOTE.")
