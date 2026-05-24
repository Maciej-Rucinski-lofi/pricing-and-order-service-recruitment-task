# Phase 0 — Prerequisites (completed)

Checklist from [PLAN.md](../PLAN.md). Status as of setup on this machine.

## 0.1 Python and virtualenv

| Item | Status | Notes |
|------|--------|-------|
| Python 3.11+ | Done | Python **3.12.10** (`python --version`) |
| Repo virtualenv | Done | `.venv/` at project root |

Activate (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

## 0.2 Graftcode Portal and Project Key

| Item | Status | Notes |
|------|--------|-------|
| Portal account | Done | [portal.graftcode.com](https://portal.graftcode.com) |
| Project | Done | `mocked-yellowstone` (per earlier gateway runs) |
| ProjectKey storage | Done | Put JWT in **`.env`** as `PROJECT_KEY` (see [.env.example](../.env.example)) — **never commit `.env`** |

Portal flow: workspace → **Create New Service** → copy Project Key → paste into `.env`.

## 0.3 Graftcode Gateway (writable install)

| Item | Status | Notes |
|------|--------|-------|
| Gateway installed | Done | `C:\Program Files\Graftcode\GraftcodeGateway\bin\gg.exe` (v1.2.7) |
| Project-local `gg` | Done | [tools/graftcode-gateway/gg.exe](../tools/graftcode-gateway/gg.exe) (gitignored, ~97 MB) |
| `Binaries.zip` fix | Done | Running `gg` from **Program Files** failed with permission error; running from `tools/graftcode-gateway/` created `Binaries.zip` successfully |

Copy gateway into project (if missing):

```powershell
.\scripts\setup-gateway.ps1
```

Smoke-test (no modules yet — confirms writable cwd):

```powershell
cd tools\graftcode-gateway
.\gg.exe
# Ctrl+C to stop; Vision would be http://localhost:81/GV when modules are added
```

**Do not** run `gg` from `C:\Program Files\Graftcode\...` for day-to-day work.

## 0.4 Academy quick-start notes (for later phases)

Skimmed tutorials relevant to this task:

| Tutorial | Link | Takeaway for this project |
|----------|------|---------------------------|
| Expose Backend (Python) | [academy …/expose-backend/python](https://academy.graftcode.com/quick-start/expose-backend/python) | Public methods on plain Python classes; `gg --modules <path>`; Vision on port **81** (`/GV`); optional `--projectKey` |
| Connect Microservices (Python) | [academy …/connect-microservices/python](https://academy.graftcode.com/quick-start/connect-microservices/python) | Install generated Graft via `pip` + extra index; configure `GraftConfig.host` or `GRAFT_CONFIG` |
| Monolith ↔ Microservices (Python) | [academy …/switch-between-monolith-and-microservices/python](https://academy.graftcode.com/quick-start/switch-between-monolith-and-microservices/python) | **LOCAL**: direct import or `GRAFT_CONFIG` with `host=inMemory`; **REMOTE**: Graft + `host=<gateway>`; switch via env only |

Core model ([Quick Start](https://academy.graftcode.com/quick-start)):

1. Expose **public methods** through Graftcode Gateway.
2. Install **generated Graft** (typed client) in the consumer.
3. Call remote methods like local code (Hypertube, not hand-written REST between services).
4. Test via **Graftcode Vision** (`http://localhost:<httpPort>/GV`).

Temporary dependency noted in academy: `hypertube-python-sdk` may be required until Graftcode stabilizes.

## Other prerequisites

| Item | Status |
|------|--------|
| Docker | Done — Docker 29.4.2 (for later Compose / academy flows) |

## Verify Phase 0

```powershell
.\scripts\verify-phase0.ps1
```

## Next step

Proceed to **Phase 1 — Project scaffold** in [PLAN.md](../PLAN.md).
