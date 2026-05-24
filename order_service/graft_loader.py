"""Load Pricing Graft client from GRAFT_CONFIG (REMOTE mode)."""

from __future__ import annotations

import importlib
import os
from typing import Any


def graft_module_name_from_config(graft_config: str) -> str:
    for segment in graft_config.split(";"):
        segment = segment.strip()
        if segment.startswith("name="):
            return segment.split("=", 1)[1].strip().replace("-", "_")
    return ""


def load_pricing_gateway_class() -> type[Any]:
    """
    Import generated Graft package and return PricingGateway class.

    Set GRAFT_PACKAGE_MODULE to override (e.g. graft_pypi_pricing_and_order_services_bbicbb).
    """
    graft_config = os.getenv("GRAFT_CONFIG", "").strip()
    if not graft_config:
        raise RuntimeError("GRAFT_CONFIG is not set")

    module_name = os.getenv("GRAFT_PACKAGE_MODULE", "").strip()
    if not module_name:
        module_name = graft_module_name_from_config(graft_config)
    if not module_name:
        raise RuntimeError("Could not parse graft module name from GRAFT_CONFIG (missing name=)")

    module = importlib.import_module(module_name)
    graft_config_cls = getattr(module, "GraftConfig", None)
    pricing_gateway = getattr(module, "PricingGateway", None)
    if graft_config_cls is None or pricing_gateway is None:
        raise RuntimeError(
            f"Module {module_name!r} must export GraftConfig and PricingGateway"
        )

    graft_config_cls.set_config(graft_config)
    return pricing_gateway
