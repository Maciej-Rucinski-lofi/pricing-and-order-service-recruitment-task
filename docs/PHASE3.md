# Phase 3 — Pricing Service (completed)

Implemented:

- `PricingService.calculate_price` — validation, discount engine, `Decimal` totals
- `calculate_discount_percent` in `pricing_service/rules.py`
- `get_product` in `pricing_service/catalog.py`
- `round_money` in `pricing_service/constants.py`

Tests: `pytest tests/test_pricing.py`

Next: **Phase 4** — expose Pricing via Graftcode Gateway and Vision.
