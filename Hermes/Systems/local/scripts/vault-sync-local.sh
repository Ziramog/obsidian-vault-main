#!/usr/bin/env bash
# Sync V6 local — safe vault synchronization for Juan's local PC.
# Works in Git Bash on Windows and in WSL if a distro exists later.
set -u

MODE="${1:---sync}"
REMOTE="${HERMES_VAULT_SYNC_REMOTE:-origin}"
BRANCH="${HERMES_VAULT_SYNC_BRANCH:-main}"
HOST_LABEL="${HERMES_VAULT_SYNC_HOST:-local}"
COMMIT_MSG="${HERMES_VAULT_SYNC_COMMIT_MSG:-auto-sync [local]}"
RETRY_MAX="${HERMES_VAULT_SYNC_RETRIES:-3}"
GIT_TIMEOUT="${HERMES_VAULT_SYNC_GIT_TIMEOUT:-60}"
LOG_FILE="${HERMES_VAULT_SYNC_LOG:-$HOME/.hermes/logs/vault-sync-local.log}"
LOCK_FILE="${HERMES_VAULT_SYNC_LOCK:-$HOME/.hermes/vault-sync-local.lock}"
LAST_GIT_OUTPUT=""
VAULT=""
COMMITTED=0
PUSHED=0

usage() {
  cat <<'USAGE'
Usage: hermes-vault-sync [--sync|--pull-only|--status|--dry-run]

Modes:
  --sync       Pull/rebase, commit local vault changes, pull again, push.
  --pull-only  Only refresh local vault from origin/main.
  --status     Print human-readable sync status.
  --dry-run    Validate environment without changing the vault.
USAGE
}

sanitize() {
  sed -E \
    -e 's#(https?://)[^/@[:space:]]+@#\1[REDACTED]@#g' \
    -e 's#(https?://[^/:[:space:]]+):[^/@[:space:]]+@#\1:[REDACTED]@#g'
}

resolve_vault() {
  if [ -n "${HERMES_VAULT_PATH:-}" ] && [ -d "$HERMES_VAULT_PATH/.git" ]; then
    VAULT="$HERMES_VAULT_PATH"
    return 0
  fi

  for candidate in \
    "/mnt/c/Projects/Obsidian/obsidian-vault-main" \
    "C:/Projects/Obsidian/obsidian-vault-main" \
    "/c/Projects/Obsidian/obsidian-vault-main"; do
    if [ -d "$candidate/.git" ]; then
      VAULT="$candidate"
      return 0
    fi
  done

  echo "ERROR: vault git repo not found. Set HERMES_VAULT_PATH." >&2
  return 64
}

ensure_dirs() {
  mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$LOCK_FILE")"
}

now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

log_line() {
  # Example: fecha host=local level=OK committed=0 pushed=0 dirty=0 ahead=0 behind=0
  local level="$1" dirty="$2" ahead="$3" behind="$4" extra="${5:-}"
  printf '%s host=%s level=%s mode=%s committed=%s pushed=%s dirty=%s ahead=%s behind=%s%s\n' \
    "$(now_iso)" "$HOST_LABEL" "$level" "$MODE" "$COMMITTED" "$PUSHED" "$dirty" "$ahead" "$behind" "${extra:+ $extra}" >> "$LOG_FILE"
}

run_git_raw() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$GIT_TIMEOUT" git -C "$VAULT" "$@"
  else
    git -C "$VAULT" "$@"
  fi
}

conflict_state() {
  [ -f "$(git -C "$VAULT" rev-parse --git-path MERGE_HEAD 2>/dev/null)" ] && return 0
  [ -d "$(git -C "$VAULT" rev-parse --git-path rebase-merge 2>/dev/null)" ] && return 0
  [ -d "$(git -C "$VAULT" rev-parse --git-path rebase-apply 2>/dev/null)" ] && return 0
  [ -f "$(git -C "$VAULT" rev-parse --git-path CHERRY_PICK_HEAD 2>/dev/null)" ] && return 0
  git -C "$VAULT" ls-files -u 2>/dev/null | grep -q . && return 0
  return 1
}

assert_no_conflict() {
  if conflict_state; then
    local dirty ahead behind
    dirty="$(dirty_count)"
    read -r behind ahead <<EOF_COUNTS
$(ahead_behind || printf '0 0')
EOF_COUNTS
    echo "ERROR: Git conflict/rebase/merge state detected. Stop; manual resolution required." >&2
    log_line "ERROR" "$dirty" "$ahead" "$behind" "conflict=1"
    return 2
  fi
}

retry_git() {
  local attempt=1 rc=0 output=""
  LAST_GIT_OUTPUT=""
  while [ "$attempt" -le "$RETRY_MAX" ]; do
    output="$(run_git_raw "$@" 2>&1)" && rc=0 || rc=$?
    output="$(printf '%s' "$output" | sanitize)"
    if [ "$rc" -eq 0 ]; then
      LAST_GIT_OUTPUT="$output"
      return 0
    fi
    LAST_GIT_OUTPUT="$output"
    if conflict_state; then
      printf 'ERROR: git %s stopped with conflict state.\n%s\n' "$*" "$LAST_GIT_OUTPUT" >&2
      return "$rc"
    fi
    if [ "$attempt" -lt "$RETRY_MAX" ]; then
      sleep $((attempt * 2))
    fi
    attempt=$((attempt + 1))
  done
  printf 'ERROR: git %s failed after %s attempts.\n%s\n' "$*" "$RETRY_MAX" "$LAST_GIT_OUTPUT" >&2
  return "$rc"
}

dirty_count() {
  git -C "$VAULT" status --porcelain 2>/dev/null | wc -l | tr -d '[:space:]'
}

ahead_behind() {
  # Prints: behind ahead
  if ! git -C "$VAULT" rev-parse --verify "$REMOTE/$BRANCH" >/dev/null 2>&1; then
    printf '0 0\n'
    return 0
  fi
  git -C "$VAULT" rev-list --left-right --count "$REMOTE/$BRANCH...HEAD" 2>/dev/null || printf '0 0\n'
}

ready_handoffs_count() {
  local count=0 f
  for f in "$VAULT"/Hermes/Handoffs/vps-to-local/*/request.md; do
    [ -f "$f" ] || continue
    if grep -Eq '^status:[[:space:]]*ready[[:space:]]*$' "$f"; then
      count=$((count + 1))
    fi
  done
  printf '%s\n' "$count"
}

remote_accessible() {
  run_git_raw ls-remote --exit-code "$REMOTE" "$BRANCH" >/dev/null 2>&1
}

pull_rebase() {
  assert_no_conflict || return $?
  retry_git pull --rebase --autostash "$REMOTE" "$BRANCH" || return $?
  assert_no_conflict || return $?
}

commit_if_dirty() {
  local dirty
  dirty="$(dirty_count)"
  if [ "$dirty" = "0" ]; then
    return 0
  fi
  retry_git add -A || return $?
  if git -C "$VAULT" diff --cached --quiet --exit-code; then
    return 0
  fi
  retry_git commit -m "$COMMIT_MSG" || return $?
  COMMITTED=1
}

push_if_ahead() {
  local behind ahead
  read -r behind ahead <<EOF_COUNTS
$(ahead_behind)
EOF_COUNTS
  if [ "${ahead:-0}" -eq 0 ]; then
    return 0
  fi
  if retry_git push "$REMOTE" "HEAD:$BRANCH"; then
    PUSHED=1
    return 0
  fi

  # One final safe retry after another rebase. Never force-push.
  pull_rebase || return $?
  retry_git push "$REMOTE" "HEAD:$BRANCH" || return $?
  PUSHED=1
}

mode_dry_run() {
  assert_no_conflict || return $?
  printf 'DRY RUN OK\n'
  printf 'Host: %s\n' "$HOST_LABEL"
  printf 'Vault: %s\n' "$VAULT"
  printf 'Branch: %s/%s\n' "$REMOTE" "$BRANCH"
  printf 'Git: %s\n' "$(command -v git)"
  printf 'Timeout command: %s\n' "$(command -v timeout 2>/dev/null || printf 'missing')"
  printf 'Lock command: %s\n' "$(command -v flock 2>/dev/null || printf 'missing; using mkdir fallback')"
  if remote_accessible; then
    printf 'GitHub: accesible\n'
  else
    printf 'GitHub: no accesible\n'
    return 69
  fi
}

mode_status() {
  local fetch_ok=0 dirty behind ahead conflicts handoffs status_icon github
  assert_no_conflict >/dev/null 2>&1 || true
  if conflict_state; then conflicts=1; else conflicts=0; fi
  if retry_git fetch --quiet "$REMOTE" "$BRANCH"; then fetch_ok=1; else fetch_ok=0; fi
  dirty="$(dirty_count)"
  read -r behind ahead <<EOF_COUNTS
$(ahead_behind)
EOF_COUNTS
  handoffs="$(ready_handoffs_count)"
  if [ "$fetch_ok" -eq 1 ]; then github="accesible"; else github="no accesible"; fi
  if [ "$dirty" = "0" ] && [ "${ahead:-0}" = "0" ] && [ "${behind:-0}" = "0" ] && [ "$conflicts" = "0" ] && [ "$fetch_ok" -eq 1 ]; then
    status_icon="✅ Vault sincronizado"
  else
    status_icon="⚠️ Vault requiere atención"
  fi
  printf '%s\n' "$status_icon"
  printf 'Host: %s\n' "$HOST_LABEL"
  printf 'GitHub: %s\n' "$github"
  printf 'Cambios pendientes: %s\n' "$dirty"
  printf 'Handoffs nuevos: %s\n' "$handoffs"
  printf 'Conflictos: %s\n' "$conflicts"
  printf 'Ahead: %s\n' "${ahead:-0}"
  printf 'Behind: %s\n' "${behind:-0}"
  printf 'Vault: %s\n' "$VAULT"
  printf 'Log: %s\n' "$LOG_FILE"
  if [ "$status_icon" = "✅ Vault sincronizado" ]; then
    log_line "OK" "$dirty" "${ahead:-0}" "${behind:-0}"
    return 0
  fi
  log_line "WARN" "$dirty" "${ahead:-0}" "${behind:-0}" "conflict=$conflicts github=$github"
  return 1
}

mode_pull_only() {
  pull_rebase || return $?
  local dirty behind ahead
  dirty="$(dirty_count)"
  read -r behind ahead <<EOF_COUNTS
$(ahead_behind)
EOF_COUNTS
  log_line "OK" "$dirty" "${ahead:-0}" "${behind:-0}"
  mode_status
}

mode_sync() {
  pull_rebase || return $?
  commit_if_dirty || return $?
  pull_rebase || return $?
  push_if_ahead || return $?
  retry_git fetch --quiet "$REMOTE" "$BRANCH" || true
  local dirty behind ahead
  dirty="$(dirty_count)"
  read -r behind ahead <<EOF_COUNTS
$(ahead_behind)
EOF_COUNTS
  if [ "$dirty" = "0" ] && [ "${ahead:-0}" = "0" ] && [ "${behind:-0}" = "0" ]; then
    log_line "OK" "$dirty" "${ahead:-0}" "${behind:-0}"
    mode_status
    return 0
  fi
  log_line "WARN" "$dirty" "${ahead:-0}" "${behind:-0}"
  mode_status
}

main_unlocked() {
  resolve_vault || return $?
  ensure_dirs
  if [ "${HERMES_VAULT_SYNC_HOLD_LOCK_SECONDS:-0}" != "0" ]; then
    sleep "$HERMES_VAULT_SYNC_HOLD_LOCK_SECONDS"
  fi
  case "$MODE" in
    --sync) mode_sync ;;
    --pull-only) mode_pull_only ;;
    --status) mode_status ;;
    --dry-run) mode_dry_run ;;
    -h|--help|help) usage ;;
    *) usage >&2; return 64 ;;
  esac
}

main() {
  ensure_dirs
  if command -v flock >/dev/null 2>&1; then
    exec 9>"$LOCK_FILE"
    if ! flock -n 9; then
      echo "ERROR: vault sync already running (flock)." >&2
      log_line "WARN" "?" "?" "?" "lock=busy"
      return 75
    fi
    main_unlocked
    return $?
  fi

  # Git Bash on this PC does not ship flock. Directory lock is the reversible fallback.
  local lock_dir="${LOCK_FILE}.d"
  if ! mkdir "$lock_dir" 2>/dev/null; then
    echo "ERROR: vault sync already running (mkdir lock fallback)." >&2
    log_line "WARN" "?" "?" "?" "lock=busy fallback=mkdir"
    return 75
  fi
  trap "rmdir '$lock_dir' 2>/dev/null || true" EXIT INT TERM
  main_unlocked
}

main "$@"
