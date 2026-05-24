# Phase 4 — Expose Pricing via Graftcode Gateway

## Hosted API

Graftcode discovers **`PricingGateway.calculate_price`** in [`pricing_service/gateway_host.py`](../pricing_service/gateway_host.py) (static method, plain `dict` return type for Vision/Graft).

Core logic remains in `PricingService`; the gateway host is a thin adapter.

## 1. Start Pricing Gateway

### Option A — Docker (recommended on Windows with Store Python)

```powershell
.\scripts\start-pricing-gateway-docker.ps1
```

- Builds the image **only the first time** (or when you pass `-Build`). The image runs `pip install` at build time (fast).
- **Mounts your repo** for live `.py` edits — **restart** the container after changes (no `pip install` on each start).
- First start can still take ~30s while Graftcode (`gg`) extracts runtimes; later restarts are much faster.
- Rebuild image only after Dockerfile or `pyproject.toml` changes: `.\scripts\start-pricing-gateway-docker.ps1 -Build`

### Option B — Native `gg.exe` on Windows

```powershell
pip install -e ".[dev]"
.\scripts\start-pricing-gateway.ps1
```

Requires a **python.org** (or similar) Python 3 install that Graftcode’s launcher can detect. The Microsoft Store Python shim often causes `Cannot find Python installed on this machine` — use Docker (option A) if you see that error.

Uses `PROJECT_KEY`, `PRICING_GATEWAY_WS_PORT` (default 9080), `PRICING_GATEWAY_HTTP_PORT` (default 9081) from `.env`.

Runs `gg` from `tools/graftcode-gateway/` (writable) with:

- `--runtime python`
- `--modules <project root>`
- `--types pricing_service.gateway_host.PricingGateway`

## 2. Graftcode Vision

Open: **http://localhost:9081/GV** (adjust port if configured).

Confirm:

- Class: `PricingGateway`
- Method: `calculate_price(product_id, quantity, customer_type)`

Use **Try it out**, e.g. `laptop`, `2`, `premium` → `total_price: 9000.0`.

## 3. Install Pricing Graft (for Order Service / REMOTE mode)

In Vision → **PyPI** tab → copy the generated `pip install` command.

Typical pattern (your URL/package name will differ):

```powershell
.\.venv\Scripts\Activate.ps1
pip install hypertube-python-sdk
pip install --extra-index-url <registry-from-vision> <graft-package-from-vision>
```

Paste `GRAFT_CONFIG` from Vision **Configuration** tab into `.env` when using REMOTE mode later.

## 4. Smoke tests

```powershell
# In-process gateway host (no Gateway required)
python scripts/smoke-pricing-graft.py

# After Graft install + GRAFT_CONFIG in .env
python scripts/smoke-pricing-graft.py
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Failed to create Binaries.zip` | Run `gg` from `tools/graftcode-gateway/`, not Program Files |
| Port in use | Change `PRICING_GATEWAY_*_PORT` in `.env` |
| Method not in Vision | Ensure `--types pricing_service.gateway_host.PricingGateway` and project root on `PYTHONPATH` |
| Import errors in Gateway | `pip install -e .` in project venv; restart gateway |
| `Cannot find Python installed` | Use Docker, or install Python from python.org (not Store-only) |
| `dockerDesktopLinuxEngine` / cannot find file | **Start Docker Desktop** and wait until running, then retry docker script |

Next: **Phase 5** — Order Service `place_order`.
