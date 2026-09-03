#!/bin/sh
set -eu

PORT="${PORT:-3000}"
exec streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port "$PORT" \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false
