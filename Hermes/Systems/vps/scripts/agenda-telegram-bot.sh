#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOT="$SCRIPT_DIR/agenda-telegram-bot.py"
ENV_FILE="/home/hermes/.hermes/.env"

has_token=0
if [[ -n "${TELEGRAM_AGENDA_BOT_TOKEN:-}" ]]; then
  has_token=1
elif [[ -f "$ENV_FILE" ]] && grep -q '^TELEGRAM_AGENDA_BOT_TOKEN=' "$ENV_FILE"; then
  has_token=1
fi

# For cron/no_agent use: keep silent when there's no dedicated bot token yet.
if [[ "$has_token" -ne 1 ]]; then
  exit 0
fi

exec python3 "$BOT" "$@"
