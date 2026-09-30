#!/usr/bin/env bash
# Enforces the local Hermes model-routing baseline. No credentials are read or written.
set -uo pipefail

HERMES_BIN='C:/Users/ingju/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe'
LOG_DIR='C:/Users/ingju/AppData/Local/hermes/model-routing-guard/logs'
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/guard-$(date '+%Y-%m-%d').log"

EXPECTED=(
  'default|opencode-go|deepseek-v4.1-flash'
  'algolab|opencode-go|deepseek-v4.1-flash'
  'algolab-darwin|opencode-go|deepseek-v4.1-flash'
  'algolab-strategy|openai-codex|gpt-5.6-sol'
  'brain-local|opencode-go|deepseek-v4.1-flash'
  'omh-test|opencode-go|deepseek-v4.1-flash'
  'pcbrain|opencode-go|deepseek-v4.1-flash'
  'trading-performance|opencode-go|deepseek-v4.1-flash'
  'web-auditor|opencode-go|deepseek-v4.1-flash'
  'web-builder|opencode-go|deepseek-v4.1-flash'
)

changed=0
failed=0
printf '%s START\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" >> "$LOG_FILE"

for spec in "${EXPECTED[@]}"; do
  IFS='|' read -r profile wanted_provider wanted_model <<< "$spec"
  actual_provider="$("$HERMES_BIN" -p "$profile" config get model.provider 2>>"$LOG_FILE" | tr -d '\r')"
  actual_model="$("$HERMES_BIN" -p "$profile" config get model.default 2>>"$LOG_FILE" | tr -d '\r')"

  if [[ "$actual_provider" != "$wanted_provider" ]]; then
    if "$HERMES_BIN" -p "$profile" config set model.provider "$wanted_provider" >> "$LOG_FILE" 2>&1; then
      changed=$((changed + 1))
    else
      printf '%s FAIL profile=%s key=model.provider expected=%s actual=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$profile" "$wanted_provider" "$actual_provider" >> "$LOG_FILE"
      failed=1
      continue
    fi
  fi

  if [[ "$actual_model" != "$wanted_model" ]]; then
    if "$HERMES_BIN" -p "$profile" config set model.default "$wanted_model" >> "$LOG_FILE" 2>&1; then
      changed=$((changed + 1))
    else
      printf '%s FAIL profile=%s key=model.default expected=%s actual=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$profile" "$wanted_model" "$actual_model" >> "$LOG_FILE"
      failed=1
      continue
    fi
  fi

  printf '%s OK profile=%s provider=%s model=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$profile" "$wanted_provider" "$wanted_model" >> "$LOG_FILE"
done

printf '%s END changes=%s failed=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$changed" "$failed" >> "$LOG_FILE"
exit "$failed"
