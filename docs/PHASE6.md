# Phase 6 — Order Service via Graftcode Vision

## Hosted API

**`OrderGateway.place_order`** and **`OrderGateway.get_order`** in [`order_service/gateway_host.py`](../order_service/gateway_host.py).

Uses `PRICING_MODE` from environment when the gateway starts (`LOCAL` by default).

## Run both gateways

Terminal 1 — Pricing (optional for LOCAL order mode):

```powershell
.\scripts\start-pricing-gateway-docker.ps1
# Vision: http://localhost:9081/GV
```

Terminal 2 — Order:

```powershell
.\scripts\start-order-gateway-docker.ps1
# Vision: http://localhost:9083/GV
```

Native `gg` (Windows): `.\scripts\start-order-gateway.ps1`

Rebuild image: `.\scripts\start-order-gateway-docker.ps1 -Build`

## Vision — Try it out

Open **http://localhost:9083/GV** (or your `ORDER_GATEWAY_HTTP_PORT`).

| Method | Inputs | Expected |
|--------|--------|----------|
| `place_order` | `laptop`, `1`, `regular` | `status: created`, `total_price: 5000` |
| `place_order` | `laptop`, `2`, `premium` | `total_price: 9000` (10% off) |
| `place_order` | `tablet`, `1`, `regular` | error — unknown product |
| `place_order` | `laptop`, `0`, `regular` | error — invalid quantity |
| `get_order` | valid `order_id` from prior call | same order |

## Troubleshooting Vision shows `(0)` methods

In the gateway terminal, look for:

```text
Found 0 classes matching type_filter: order_service.gateway_host.OrderGateway
```

That means `OrderGateway` did not load (often `ImportError` on `gateway_host` during analysis). Restart the order gateway after code fixes. Pricing Vision (`9081`) and Order Vision (`9083`) are **separate** — order methods only appear on the order port.

## REMOTE pricing through Order Gateway

1. Start **Pricing** gateway (`9080`/`9081`).
2. Install Pricing Graft from **local** Vision (`http://localhost:9081/GV`).
3. Set in `.env`: `PRICING_MODE=REMOTE` and `GRAFT_CONFIG=...` from Vision.
4. Restart Order gateway so it picks up env.

## Ports (default)

| Service | WebSocket | Vision |
|---------|-----------|--------|
| Pricing | 9080 | http://localhost:9081/GV |
| Order | 9082 | http://localhost:9083/GV |
