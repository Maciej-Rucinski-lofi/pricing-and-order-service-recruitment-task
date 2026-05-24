#!/bin/sh
set -e

# Package is installed at image build. Bind mount updates .py files without pip on each start.
# Rebuild image (-Build) only after pyproject.toml / dependency changes.
# Optional: PIP_INSTALL_ON_START=1 to force editable reinstall (slow on Windows mounts).
if [ "${PIP_INSTALL_ON_START:-0}" = "1" ] && [ -f /app/pyproject.toml ]; then
  pip install -e /app -q
fi

exec gg --runtime python \
  --modules /app \
  --types pricing_service.gateway_host.PricingGateway \
  --port 9080 \
  --httpPort 9081 \
  ${PROJECT_KEY:+--projectKey "$PROJECT_KEY"}
