# Phase 5 — Order Service (completed)

## Implemented

- `OrderService.place_order` — pricing via `PricingClient`, persist on success only
- `LocalPricingClient` / `RemotePricingClient` (Graft + retries)
- `build_order_service()` — uses `PRICING_MODE` from `.env`
- `tests/test_order.py`

## Usage

```powershell
# LOCAL (default)
$env:PRICING_MODE = "LOCAL"
python -c "from order_service import build_order_service; o=build_order_service(); print(o.place_order('mouse',1,'regular'))"

# REMOTE (after Graft install + GRAFT_CONFIG in .env)
$env:PRICING_MODE = "REMOTE"
python -c "from order_service import build_order_service; print(build_order_service().place_order('mouse',1,'regular'))"
```

Next: **Phase 6** — expose `place_order` via Order Gateway + Vision.
