#!/usr/bin/env bash
set -e
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="dev-only-token"

vault kv put secret/gateway \
  backend_shared_secret="gateway-api-secret-456" \
  auth_introspection_secret="gateway-auth-secret-789"

vault kv get secret/gateway
