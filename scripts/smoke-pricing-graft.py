#!/usr/bin/env python3
"""
Smoke-test Pricing via generated Graft (Phase 4).

Prerequisites:
  1. Pricing Gateway running: .\\scripts\\start-pricing-gateway.ps1
  2. Install Graft from Vision (PyPI tab) — copy the pip command shown at:
     http://localhost:9081/GV  (or your PRICING_GATEWAY_HTTP_PORT)

Example Vision install (URLs vary per project):
  pip install hypertube-python-sdk
  pip install --extra-index-url https://grft.dev/... @graft/pypi-pricinggateway@...

Then set GRAFT_CONFIG or GraftConfig.host per Vision Configuration tab and run:
  python scripts/smoke-pricing-graft.py
"""

from __future__ import annotations

import os
import sys


def smoke_local_host() -> None:
    """Always available — validates gateway_host without Graft."""
    from pricing_service.gateway_host import PricingGateway

    from decimal import Decimal

    result = PricingGateway.calculate_price("laptop", 2, "premium")
    print("Local PricingGateway:", result)
    assert result.total_price == Decimal("9000.00")


def smoke_graft() -> None:
    graft_config = os.getenv("GRAFT_CONFIG", "").strip()
    if not graft_config:
        print(
            "GRAFT_CONFIG not set — skipping remote Graft call.\n"
            "Install the Pricing Graft from Vision and set GRAFT_CONFIG in .env.",
            file=sys.stderr,
        )
        return

    # Import path depends on Vision-generated package name (update after install).
    try:
        from graft_pypi_pricinggateway import GraftConfig, PricingGateway  # type: ignore
    except ImportError as exc:
        print(
            "Pricing Graft not installed. Install from Vision PyPI tab, then re-run.\n"
            f"Import error: {exc}",
            file=sys.stderr,
        )
        return

    GraftConfig.set_config(graft_config)
    result = PricingGateway.calculate_price("mouse", 10, "regular")
    print("Remote Graft PricingGateway:", result)


if __name__ == "__main__":
    smoke_local_host()
    smoke_graft()
