# Pricing & Order Services (Graftcode recruitment task)

Two Python services — **Pricing** and **Order** — connected via [Graftcode](https://graftcode.com) in REMOTE mode, with LOCAL in-process mode for a modular monolith.

## Status

| Phase | Status |
|-------|--------|
| 0 — Prerequisites | Done — [docs/PHASE0.md](docs/PHASE0.md) |
| 1 — Project scaffold | Done — this layout |
| 2 — Domain decisions | Done — below |
| 3 — Pricing core | Done — `pytest tests/test_pricing.py` |
| 4 — Pricing Graftcode | Done — [docs/PHASE4.md](docs/PHASE4.md) |
| 5 — Order core | Done — `pytest tests/test_order.py` |
| 6 — Order Graftcode | Done — [docs/PHASE6.md](docs/PHASE6.md) |
| 7+ | See [PLAN.md](PLAN.md) |

## Project layout

```
pricing_service/   # calculate_price (Graftcode-hosted)
order_service/     # place_order (Vision-tested)
config/            # products.json, pricing_rules.json
tests/
tools/graftcode-gateway/   # local gg.exe (not in git)
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env   # set PROJECT_KEY from portal.graftcode.com
.\scripts\setup-gateway.ps1   # copy gg.exe if missing
```

## Run tests

```powershell
pytest
pytest tests/test_pricing.py
```

### Try pricing locally (Python)

```powershell
python -c "from pricing_service import PricingService; p=PricingService(); r=p.calculate_price('laptop',2,'premium'); print(r)"
```

## Configuration

See [.env.example](.env.example): `PROJECT_KEY`, `PRICING_MODE` (`LOCAL` \| `REMOTE`), `GRAFT_CONFIG`, gateway ports.

## Domain decisions

These rules are fixed before implementing pricing/order logic (Phase 3+). Constants live in [`pricing_service/constants.py`](pricing_service/constants.py).

### Money

- Use **`decimal.Decimal`** for unit prices, discounts, and totals inside both services.
- Load catalog prices from JSON as strings/decimals, not binary floats.
- Convert to `float` only at Graftcode or API boundaries if the hosted runtime requires it.

### Discount stacking

- **Customer discount** and **quantity discount** percentages are **additive**, not compounded.
- **Cap:** total discount cannot exceed **20%** (`max_total_discount_percent` in [`config/pricing_rules.json`](config/pricing_rules.json)).
- **Example:** `premium` (10%) + quantity ≥ 10 (5%) → **15%** off; not 14.5% compounded.

### Rounding

- `total_price` is rounded to **2 decimal places** with **`ROUND_HALF_UP`** (banker's half-up for positive money amounts).

### Validation vs infrastructure errors

| Situation | Type | Order Service behavior |
|-----------|------|------------------------|
| Unknown `product_id` | Validation (`UnknownProductError`) | Do not persist order; clear message to caller |
| `quantity` ≤ 0 | Validation (`InvalidQuantityError`) | Do not persist order |
| Unsupported `customer_type` | Validation (`UnsupportedCustomerTypeError`) | Do not persist order |
| Pricing Gateway / Graft down | Infrastructure (`PricingUnavailableError`) | Do not persist order; log with context |

Validation errors originate in Pricing; Order Service must not save partial orders when pricing fails.

### Edge cases

| Case | Decision |
|------|----------|
| Quantity `0` or negative | Reject — only integers **≥ 1** are valid |
| Unknown product | Reject — product must exist in [`config/products.json`](config/products.json) |
| Unsupported `customer_type` | Reject — must be a key in `customer_discounts` in rules JSON |
| Malformed `products.json` | Fail at startup when catalog is loaded (not per-request) |
| Malformed `pricing_rules.json` | Fail at startup when rules are loaded |
| Empty product catalog | Fail at startup |

### Configurable pricing rules

Rules are **not** embedded in `calculate_price`. They live in **`config/pricing_rules.json`** and are loaded by [`pricing_service/rules.py`](pricing_service/rules.py).

**Why JSON:** same structure as `products.json`, no extra dependencies, easy to extend with new `customer_discounts` keys or `quantity_discounts` tiers. The engine applies customer % + best matching quantity tier %, then caps the sum.

To add a rule: edit JSON (e.g. new `"vip": 15` under `customer_discounts`) and restart; no change to calculation flow structure.

### Error representation (planned)

- Pricing: typed exceptions in [`pricing_service/exceptions.py`](pricing_service/exceptions.py).
- Order: wraps infrastructure failures in [`order_service/exceptions.py`](order_service/exceptions.py); validation errors propagate from Pricing.

## Graftcode — Pricing Service (Phase 4)

```powershell
pip install -e ".[dev]"
.\scripts\start-pricing-gateway-docker.ps1   # rebuild only: add -Build
# or native: .\scripts\start-pricing-gateway.ps1
```

Open **http://localhost:9081/GV** → `PricingGateway.calculate_price` → Try it out.

Install the generated **Graft** from Vision (PyPI tab) for REMOTE mode later. Details: [docs/PHASE4.md](docs/PHASE4.md).

```powershell
python scripts/smoke-pricing-graft.py
```

### Try orders locally

```powershell
$env:PRICING_MODE = "LOCAL"
python -c "from order_service import build_order_service; print(build_order_service().place_order('laptop',1,'regular'))"
```

See [docs/PHASE5.md](docs/PHASE5.md) for REMOTE mode with Graft.

## Graftcode — Order Service (Phase 6)

```powershell
.\scripts\start-order-gateway-docker.ps1
```

Open **http://localhost:9083/GV** and test `OrderGateway.place_order` (e.g. `laptop`, `1`, `regular`).

Run Pricing gateway on `9081` in another terminal if using `PRICING_MODE=REMOTE`. Details: [docs/PHASE6.md](docs/PHASE6.md).
