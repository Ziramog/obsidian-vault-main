#!/usr/bin/env bash
# Robust Obsidian vault synchronization for brain-local / pc-ops on Windows.
# Git Bash fallback implementation because this host has wsl.exe but no registered WSL distro.

set -uo pipefail

export PATH="/mingw64/bin:/usr/bin:/bin:$PATH"
export GIT_TERMINAL_PROMPT=0

MODE="${1:---sync}"
VAULT="${HERMES_VAULT:-C:/Projects/Obsidian/obsidian-vault-main}"
HOST_TAG="${HERMES_SYNC_HOST:-local}"
LOG_DIR="${HERMES_LOG_DIR:-$HOME/.hermes/logs}"
LOG_FILE="${LOG_DIR}/vault-sync-local.log"
LOCK_ROOT="${HERMES_LOCK_DIR:-$HOME/.cache/hermes}"
LOCK_NAME="hermes-vault-sync-local"
LOCK_FILE="${LOCK_ROOT}/${LOCK_NAME}.lock"
LOCK_PATH="${LOCK_ROOT}/${LOCK_NAME}.lockdir"
GIT_BIN="${GIT_BIN:-git}"
TIMEOUT_BIN="${TIMEOUT_BIN:-timeout}"
MAX_ATTEMPTS="${HERMES_SYNC_ATTEMPTS:-3}"
OP_TIMEOUT="${HERMES_SYNC_TIMEOUT:-120}"
STALE_LOCK_SECONDS="${HERMES_SYNC_STALE_LOCK_SECONDS:-1800}"
LOCK_BACKEND="none"
LOCK_ACQUIRED="0"

mkdir -p "$LOG_DIR" "$LOCK_ROOT"
touch "$LOG_FILE"
chmod 600 "$LOG_FILE" 2>/dev/null || true

sanitize_stream() {
  sed -E 's#(https?://)[^/@]+@#\1***@#g; s#(gho_|ghp_|github_pat_)[A-Za-z0-9_]+#***#g; s#([Tt]oken: )[A-Za-z0-9_./=-]+#\1***#g'
}

compact() {
  tr '\r\n' ' ' | tr -s ' ' | sanitize_stream | cut -c1-700
}

log() {
  local level="$1"
  shift
  printf '%s host=%s level=%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%:z')" "$HOST_TAG" "$level" "$*" | tee -a "$LOG_FILE"
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log ERROR "missing_command=$1"
    exit 20
  fi
}

for required in "$GIT_BIN" "$TIMEOUT_BIN" date tee tr cut wc sleep mkdir find grep; do
  require_command "$required"
done

if [[ ! -d "$VAULT/.git" ]]; then
  log ERROR "not_git_repo vault=$VAULT"
  exit 21
fi

lock_backend_name() {
  if command -v flock >/dev/null 2>&1; then
    printf 'flock'
  else
    printf 'mkdir-fallback'
  fi
}

release_lock() {
  if [[ "$LOCK_ACQUIRED" == "1" && "$LOCK_BACKEND" == "mkdir" && -d "$LOCK_PATH" ]]; then
    rm -f "$LOCK_PATH/pid" "$LOCK_PATH/acquired_epoch" "$LOCK_PATH/acquired_at" 2>/dev/null || true
    rmdir "$LOCK_PATH" 2>/dev/null || true
  fi
}

acquire_lock() {
  if command -v flock >/dev/null 2>&1; then
    exec 9>"$LOCK_FILE"
    if flock -n 9; then
      LOCK_BACKEND="flock"
      LOCK_ACQUIRED="1"
      return 0
    fi
    log SKIP "reason=lock_busy backend=flock"
    return 1
  fi

  LOCK_BACKEND="mkdir"
  local now acquired age
  now="$(date +%s)"
  if mkdir "$LOCK_PATH" 2>/dev/null; then
    printf '%s\n' "$$" > "$LOCK_PATH/pid"
    printf '%s\n' "$now" > "$LOCK_PATH/acquired_epoch"
    date '+%Y-%m-%dT%H:%M:%S%:z' > "$LOCK_PATH/acquired_at"
    LOCK_ACQUIRED="1"
    trap release_lock EXIT INT TERM
    return 0
  fi

  acquired="$(cat "$LOCK_PATH/acquired_epoch" 2>/dev/null || printf '0')"
  if [[ "$acquired" =~ ^[0-9]+$ && "$acquired" != "0" ]]; then
    age=$((now - acquired))
  else
    age=0
  fi

  if [[ "$age" -gt "$STALE_LOCK_SECONDS" && "$LOCK_PATH" == *"${LOCK_NAME}.lockdir" ]]; then
    log WARN "reason=stale_lock age_seconds=$age action=remove_lock_dir backend=mkdir-fallback"
    rm -f "$LOCK_PATH/pid" "$LOCK_PATH/acquired_epoch" "$LOCK_PATH/acquired_at" 2>/dev/null || true
    rmdir "$LOCK_PATH" 2>/dev/null || true
    if mkdir "$LOCK_PATH" 2>/dev/null; then
      printf '%s\n' "$$" > "$LOCK_PATH/pid"
      printf '%s\n' "$now" > "$LOCK_PATH/acquired_epoch"
      date '+%Y-%m-%dT%H:%M:%S%:z' > "$LOCK_PATH/acquired_at"
      LOCK_ACQUIRED="1"
      trap release_lock EXIT INT TERM
      return 0
    fi
  fi

  log SKIP "reason=lock_busy backend=mkdir-fallback age_seconds=$age"
  return 1
}

has_git_operation_in_progress() {
  [[ -d "$VAULT/.git/rebase-merge" || -d "$VAULT/.git/rebase-apply" || -f "$VAULT/.git/MERGE_HEAD" || -f "$VAULT/.git/CHERRY_PICK_HEAD" ]]
}

unmerged_files() {
  "$GIT_BIN" -C "$VAULT" diff --name-only --diff-filter=U 2>/dev/null
}

conflict_count() {
  local op unresolved count
  op=0
  has_git_operation_in_progress && op=1
  unresolved="$(unmerged_files | wc -l | tr -d ' ')"
  count=$((op + unresolved))
  printf '%s' "$count"
}

ensure_safe_state() {
  local unresolved
  if has_git_operation_in_progress; then
    log ERROR "git_operation_in_progress action=manual_review"
    return 1
  fi
  unresolved="$(unmerged_files)"
  if [[ -n "$unresolved" ]]; then
    log ERROR "unmerged_files=$(printf '%s' "$unresolved" | compact) action=manual_review"
    return 1
  fi
  return 0
}

run_with_retry() {
  local label="$1"
  shift
  local attempt=1
  local output rc
  while (( attempt <= MAX_ATTEMPTS )); do
    output="$($TIMEOUT_BIN "$OP_TIMEOUT" "$@" 2>&1)"
    rc=$?
    if (( rc == 0 )); then
      [[ -n "$output" ]] && log INFO "$label=$(printf '%s' "$output" | compact)"
      return 0
    fi
    log WARN "operation=$label attempt=$attempt rc=$rc output=$(printf '%s' "$output" | compact)"
    if has_git_operation_in_progress || [[ -n "$(unmerged_files)" ]]; then
      ensure_safe_state >/dev/null
      return 1
    fi
    if (( attempt < MAX_ATTEMPTS )); then
      sleep $((attempt * 5))
    fi
    attempt=$((attempt + 1))
  done
  return 1
}

pull_latest() {
  ensure_safe_state || return 1
  if ! run_with_retry pull "$GIT_BIN" -C "$VAULT" pull --rebase --autostash origin main; then
    log ERROR "operation=pull result=failed attempts=$MAX_ATTEMPTS"
    return 1
  fi
  ensure_safe_state || return 1
  return 0
}

repo_counts() {
  local dirty ahead behind
  dirty="$($GIT_BIN -C "$VAULT" status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ')"
  ahead="$($GIT_BIN -C "$VAULT" rev-list --count origin/main..HEAD 2>/dev/null || printf '?')"
  behind="$($GIT_BIN -C "$VAULT" rev-list --count HEAD..origin/main 2>/dev/null || printf '?')"
  printf 'dirty=%s ahead=%s behind=%s' "$dirty" "$ahead" "$behind"
}

pending_handoffs_count() {
  local root req dir count
  root="$VAULT/Hermes/Handoffs/vps-to-local"
  count=0
  [[ -d "$root" ]] || { printf '0'; return 0; }
  while IFS= read -r req; do
    dir="$(dirname "$req")"
    if grep -q '^status: ready' "$req" 2>/dev/null && [[ ! -f "$dir/response.md" ]]; then
      count=$((count + 1))
    fi
  done < <(find "$root" -mindepth 2 -maxdepth 2 -name request.md -type f 2>/dev/null)
  printf '%s' "$count"
}

github_access() {
  if "$TIMEOUT_BIN" 45 "$GIT_BIN" -C "$VAULT" ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
    printf 'accesible'
  else
    printf 'no_accesible'
  fi
}

show_status() {
  local counts dirty ahead behind gh handoffs conflicts icon title
  counts="$(repo_counts)"
  dirty="$(printf '%s' "$counts" | sed -n 's/.*dirty=\([^ ]*\).*/\1/p')"
  ahead="$(printf '%s' "$counts" | sed -n 's/.*ahead=\([^ ]*\).*/\1/p')"
  behind="$(printf '%s' "$counts" | sed -n 's/.*behind=\([^ ]*\).*/\1/p')"
  gh="$(github_access)"
  handoffs="$(pending_handoffs_count)"
  conflicts="$(conflict_count)"
  if [[ "$dirty" == "0" && "$ahead" == "0" && "$behind" == "0" && "$conflicts" == "0" && "$gh" == "accesible" ]]; then
    icon="✅"
    title="Vault sincronizado"
  else
    icon="⚠️"
    title="Vault requiere atencion"
  fi
  printf '%s %s\n' "$icon" "$title"
  printf 'Host: %s\n' "$HOST_TAG"
  printf 'GitHub: %s\n' "$gh"
  printf 'Cambios pendientes: %s\n' "$dirty"
  printf 'Handoffs nuevos: %s\n' "$handoffs"
  printf 'Conflictos: %s\n' "$conflicts"
  printf 'Detalle: ahead=%s behind=%s log=%s\n' "$ahead" "$behind" "$LOG_FILE"
  log STATUS "$counts github=$gh handoffs_new=$handoffs conflicts=$conflicts lock_backend=$(lock_backend_name) vault=$VAULT"
  [[ "$icon" == "✅" ]]
}

case "$MODE" in
  --dry-run)
    log OK "dry_run=passed vault=$VAULT log=$LOG_FILE lock_backend=$(lock_backend_name) note=no_wsl_distro_git_bash_fallback"
    exit 0
    ;;
  --status)
    show_status
    exit $?
    ;;
  --pull-only|--sync)
    ;;
  *)
    log ERROR "unknown_mode=$MODE expected=--sync|--pull-only|--status|--dry-run"
    exit 22
    ;;
esac

if ! acquire_lock; then
  if [[ "$MODE" == "--pull-only" ]]; then
    exit 75
  fi
  exit 0
fi

if [[ "${HERMES_SYNC_TEST_HOLD_SECONDS:-0}" =~ ^[0-9]+$ && "${HERMES_SYNC_TEST_HOLD_SECONDS:-0}" -gt 0 ]]; then
  log INFO "test_lock_hold_seconds=${HERMES_SYNC_TEST_HOLD_SECONDS}"
  sleep "${HERMES_SYNC_TEST_HOLD_SECONDS}"
fi

case "$MODE" in
  --pull-only)
    if pull_latest; then
      log OK "mode=pull-only $(repo_counts)"
      exit 0
    fi
    exit 30
    ;;
esac

if ! pull_latest; then
  exit 30
fi

if ! "$GIT_BIN" -C "$VAULT" add -A; then
  log ERROR "operation=add result=failed"
  exit 31
fi

committed=0
"$GIT_BIN" -C "$VAULT" diff --cached --quiet
staged_rc=$?
if (( staged_rc == 1 )); then
  commit_output="$("$GIT_BIN" -C "$VAULT" commit -m "auto-sync [$HOST_TAG]" 2>&1)"
  commit_rc=$?
  if (( commit_rc != 0 )); then
    log ERROR "operation=commit rc=$commit_rc output=$(printf '%s' "$commit_output" | compact)"
    exit 33
  fi
  committed=1
  log INFO "commit=$(printf '%s' "$commit_output" | compact)"
elif (( staged_rc > 1 )); then
  log ERROR "operation=staged_diff rc=$staged_rc"
  exit 32
fi

# Close the race window: another host may have pushed after our first pull.
if ! pull_latest; then
  exit 34
fi

pushed=0
ahead="$($GIT_BIN -C "$VAULT" rev-list --count origin/main..HEAD 2>/dev/null || printf '0')"
if [[ "$ahead" != "0" ]]; then
  if run_with_retry push "$GIT_BIN" -C "$VAULT" push origin main; then
    pushed=1
  else
    # One final rebase+push cycle for a non-fast-forward race.
    log WARN "operation=push retry_after_pull=true"
    if pull_latest && run_with_retry push-final "$GIT_BIN" -C "$VAULT" push origin main; then
      pushed=1
    else
      log ERROR "operation=push result=failed action=manual_review"
      exit 35
    fi
  fi
fi

counts="$(repo_counts)"
if [[ "$counts" == "dirty=0 ahead=0 behind=0" ]]; then
  log OK "mode=sync committed=$committed pushed=$pushed $counts"
  exit 0
fi

log WARN "mode=sync committed=$committed pushed=$pushed $counts action=inspect"
exit 36
