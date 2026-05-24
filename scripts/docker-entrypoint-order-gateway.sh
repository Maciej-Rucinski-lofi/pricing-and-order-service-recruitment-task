#!/bin/sh
set -e

if [ "${PIP_INSTALL_ON_START:-0}" = "1" ] && [ -f /app/pyproject.toml ]; then
  pip install -e /app -q
fi

exec gg --runtime python \
  --modules /app \
  --types order_service.gateway_host.OrderGateway \
  --port 9082 \
  --httpPort 9083 \
  ${PROJECT_KEY:+--projectKey "$PROJECT_KEY"}
