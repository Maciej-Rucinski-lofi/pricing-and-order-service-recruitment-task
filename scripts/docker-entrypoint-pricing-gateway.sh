#!/bin/sh
set -e

# Project is bind-mounted at /app - pick up Python changes without rebuilding the image.
if [ -f /app/pyproject.toml ]; then
  pip install -e /app -q
fi

exec gg --runtime python \
  --modules /app \
  --types pricing_service.gateway_host.PricingGateway \
  --port 9080 \
  --httpPort 9081 \
  ${PROJECT_KEY:+--projectKey "$PROJECT_KEY"}
