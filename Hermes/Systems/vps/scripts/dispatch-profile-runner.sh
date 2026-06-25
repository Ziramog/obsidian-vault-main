#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# dispatch-profile-runner.sh — Runner interno para background mode
# Ejecuta la tarea y maneja el cleanup
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

PROFILE="$1"
TASK_FILE="$2"
RUNNING_FILE="$3"
OUTPUT_FILE="$4"
TASK_BASENAME="$5"
TIMESTAMP="$6"

VAULT="/home/hermes/obsidian-vault"
TASKS_DIR="$VAULT/Hermes/Tasks"

TASK_CONTENT=$(cat "$TASK_FILE")

# Ejecutar
exit_code=0
hermes chat --profile "$PROFILE" -q "$TASK_CONTENT" --quiet 2>&1 | tee "$OUTPUT_FILE" || exit_code=$?

# Cleanup
rm -f "$RUNNING_FILE"

if [ "$exit_code" -eq 0 ]; then
    echo "✓ Task completada (exit 0)"
    echo "  Output: $OUTPUT_FILE"
else
    FAILED_FILE="$TASKS_DIR/failed/${TASK_BASENAME}.md"
    cp "$TASK_FILE" "$FAILED_FILE"
    echo "✗ Task falló (exit $exit_code)"
    echo "  Output: $OUTPUT_FILE"
fi