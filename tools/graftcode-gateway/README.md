# Graftcode Gateway (local copy)

Run the gateway from **this directory** so `Binaries.zip` and extracted runtimes are written here (writable), not under `Program Files`.

`gg.exe` is not in git (~97 MB). Install once:

```powershell
..\..\scripts\setup-gateway.ps1
```

Prefer the project script (loads `.env`, sets Python PATH):

```powershell
..\..\scripts\start-pricing-gateway.ps1
```

Vision: `http://localhost:9081/GV` — class `PricingGateway`, method `calculate_price`.
