#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# dispatch-profile.sh — Mecanismo de activación inter-perfiles VPS
# brain-vps usa este script para despachar tareas a profiles VPS
# ═══════════════════════════════════════════════════════════════
#
# Uso:
#   ./dispatch-profile.sh <profile> <task-file> [--background]
#
# Donde:
#   profile     = Nombre del perfil (ango-comercial, wolfim-growth, etc.)
#   task-file   = Path absoluto al archivo .md con la tarea
#   --background = (opcional) Ejecutar en background con tmux
#
# El script:
#   1. Lee el task-file
#   2. Mueve el task a Hermes/Tasks/running/
#   3. Ejecuta: hermes chat --profile <profile> -q "<contenido del task>"
#   4. Captura stdout al archivo de output
#   5. Mueve el task a completed/ o failed/ según resultado
#   6. El resultado queda en Hermes/Tasks/completed/<task-id>-output.md
#
# Retornos:
#   0 = Éxito
#   1 = Error de parámetros
#   2 = Error de ejecución
#
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

VAULT="/home/hermes/obsidian-vault"
TASKS_DIR="$VAULT/Hermes/Tasks"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── Validar parámetros ───
if [ $# -lt 2 ]; then
    echo "ERROR: Uso: $0 <profile> <task-file> [--background]"
    echo ""
    echo "Profiles disponibles en VPS:"
    ls "$HOME/.hermes/profiles/" 2>/dev/null | grep -v "^\." | sed 's/^/  - /'
    exit 1
fi

PROFILE="$1"
TASK_FILE="$2"
BACKGROUND="false"

if [ "${3:-}" = "--background" ]; then
    BACKGROUND="true"
fi

# ─── Validar que el perfil existe ───
PROFILE_DIR="$HOME/.hermes/profiles/$PROFILE"
if [ ! -d "$PROFILE_DIR" ]; then
    echo "ERROR: Perfil '$PROFILE' no existe en $HOME/.hermes/profiles/"
    echo "Perfiles disponibles:"
    ls "$HOME/.hermes/profiles/" 2>/dev/null | grep -v "^\." | sed 's/^/  - /'
    exit 1
fi

# ─── Validar que el task-file existe ───
if [ ! -f "$TASK_FILE" ]; then
    echo "ERROR: Task file no existe: $TASK_FILE"
    exit 1
fi

# ─── Generar task ID ───
TASK_ID=$(basename "$TASK_FILE" .md)
TASK_BASENAME="${TASK_ID}"
OUTPUT_FILE="$TASKS_DIR/completed/${TASK_BASENAME}-${TIMESTAMP}-output.md"

# ─── Mover task a running/ ───
RUNNING_FILE="$TASKS_DIR/running/${TASK_BASENAME}.md"
cp "$TASK_FILE" "$RUNNING_FILE"

# Escribir metadata al inicio del running file
cat > "$RUNNING_FILE" << EOF
---
task-id: $TASK_BASENAME
profile: $PROFILE
status: running
started-at: $TIMESTAMP
source: $(basename "$TASK_FILE")
---

EOF

cat "$TASK_FILE" >> "$RUNNING_FILE"

# ─── Leer contenido del task ───
TASK_CONTENT=$(cat "$TASK_FILE")

# ─── Función de ejecución ───
run_task() {
    local exit_code=0
    
    # Ejecutar hermes con el perfil y la tarea
    # --quiet suprime banner/spinner
    # -q pasa el prompt como query única (non-interactive)
    hermes chat --profile "$PROFILE" -q "$TASK_CONTENT" --quiet 2>&1 | tee "$OUTPUT_FILE" || exit_code=$?
    
    return $exit_code
}

# ─── Ejecutar ───
echo "═══ DISPATCH ═══"
echo "Profile: $PROFILE"
echo "Task:    $TASK_BASENAME"
echo "Started: $TIMESTAMP"
echo ""

if [ "$BACKGROUND" = "true" ]; then
    # Ejecutar en tmux para no bloquear
    SESSION_NAME="task-${TASK_BASENAME}-${TIMESTAMP}"
    tmux new-session -d -s "$SESSION_NAME" -x 120 -y 40 \
        "bash $SCRIPT_DIR/dispatch-profile-runner.sh '$PROFILE' '$TASK_FILE' '$RUNNING_FILE' '$OUTPUT_FILE' '$TASK_BASENAME' '$TIMESTAMP'; echo 'PRESIONE ENTER PARA CERRAR'; read"
    echo "✓ Task enviada a background (tmux session: $SESSION_NAME)"
    echo "  Para ver: tmux attach -t $SESSION_NAME"
    echo "  Para cerrar: tmux kill-session -t $SESSION_NAME"
else
    # Ejecutar en foreground
    run_task
    EXIT_CODE=$?
    
    # ─── Mover task según resultado ───
    rm "$RUNNING_FILE"
    
    if [ $EXIT_CODE -eq 0 ]; then
        COMPLETED_FILE="$TASKS_DIR/completed/${TASK_BASENAME}.md"
        echo "✓ Task completada. Output en: $OUTPUT_FILE"
    else
        FAILED_FILE="$TASKS_DIR/failed/${TASK_BASENAME}.md"
        cp "$TASK_FILE" "$FAILED_FILE"
        echo "✗ Task falló (exit $EXIT_CODE). Output en: $OUTPUT_FILE"
    fi
fi