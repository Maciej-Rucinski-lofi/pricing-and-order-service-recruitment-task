# Graftcode Gateway (local copy)

Run the gateway from **this directory** so `Binaries.zip` and extracted runtimes are written here (writable), not under `Program Files`.

`gg.exe` is not in git (~97 MB). Install once:

```powershell
..\..\scripts\setup-gateway.ps1
```

Example (after Pricing module exists in Phase 4):

```powershell
$env:PROJECT_KEY = "<from .env>"
.\gg.exe --projectKey $env:PROJECT_KEY --runtime python --modules ..\..\pricing_service --port 9080 --httpPort 9081
```

Vision: `http://localhost:9081/GV`
