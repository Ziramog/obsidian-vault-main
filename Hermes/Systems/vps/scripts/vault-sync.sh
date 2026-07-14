#!/usr/bin/env bash
# Robust Obsidian vault synchronization for brain-vps.
# Agents write files; this independent process owns Git operations.

set -uo pipefail

MODE="${1:---sync}"
VAULT="${HERMES_VAULT:-/home/hermes/obsidian-vault}"
HOST_TAG="${HERMES_SYNC_HOST:-vps}"
LOG_DIR="${HERMES_LOG_DIR:-/home/hermes/.hermes/logs}"
LOG_FILE="${LOG_DIR}/vault-sync-${HOST_TAG}.log"
LOCK_DIR="${XDG_CACHE_HOME:-/home/hermes/.cache}"
LOCK_FILE="${LOCK_DIR}/hermes-vault-sync-${HOST_TAG}.lock"
GIT_BIN="${GIT_BIN:-/usr/bin/git}"
TIMEOUT_BIN="${TIMEOUT_BIN:-/usr/bin/timeout}"
MAX_ATTEMPTS="${HERMES_SYNC_ATTEMPTS:-3}"

mkdir -p "$LOG_DIR" "$LOCK_DIR"
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"

log() {
  local level="$1"
  shift
  printf '%s host=%s level=%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%:z')" "$HOST_TAG" "$level" "$*" | tee -a "$LOG_FILE"
}

compact() {
  tr '\n' ' ' | tr -s ' ' | cut -c1-700
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log ERROR "missing_command=$1"
    exit 20
  fi
}

for required in "$GIT_BIN" "$TIMEOUT_BIN" flock date tee tr cut wc sleep; do
  require_command "$required"
done

if [[ ! -d "$VAULT/.git" ]]; then
  log ERROR "not_git_repo vault=$VAULT"
  exit 21
fi

if [[ "$MODE" == "--dry-run" ]]; then
  log OK "dry_run=passed vault=$VAULT log=$LOG_FILE lock=$LOCK_FILE"
  exit 0
fi

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  log SKIP "reason=lock_busy"
  exit 0
fi

has_git_operation_in_progress() {
  [[ -d "$VAULT/.git/rebase-merge" || -d "$VAULT/.git/rebase-apply" || -f "$VAULT/.git/MERGE_HEAD" || -f "$VAULT/.git/CHERRY_PICK_HEAD" ]]
}

unmerged_files() {
  "$GIT_BIN" -C "$VAULT" diff --name-only --diff-filter=U
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
    output="$($TIMEOUT_BIN 120 "$@" 2>&1)"
    rc=$?
    if (( rc == 0 )); then
      [[ -n "$output" ]] && log INFO "$label=$(printf '%s' "$output" | compact)"
      return 0
    fi
    log WARN "operation=$label attempt=$attempt rc=$rc output=$(printf '%s' "$output" | compact)"
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
  dirty="$($GIT_BIN -C "$VAULT" status --porcelain=v1 | wc -l | tr -d ' ')"
  ahead="$($GIT_BIN -C "$VAULT" rev-list --count origin/main..HEAD 2>/dev/null || printf '?')"
  behind="$($GIT_BIN -C "$VAULT" rev-list --count HEAD..origin/main 2>/dev/null || printf '?')"
  printf 'dirty=%s ahead=%s behind=%s' "$dirty" "$ahead" "$behind"
}

show_status() {
  local counts
  ensure_safe_state || exit 1
  counts="$(repo_counts)"
  log STATUS "$counts vault=$VAULT"
}

case "$MODE" in
  --status)
    show_status
    exit 0
    ;;
  --pull-only)
    if pull_latest; then
      log OK "mode=pull-only $(repo_counts)"
      exit 0
    fi
    exit 30
    ;;
  --sync)
    ;;
  *)
    log ERROR "unknown_mode=$MODE expected=--sync|--pull-only|--status|--dry-run"
    exit 22
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
  check_output="$($GIT_BIN -C "$VAULT" diff --cached --check 2>&1)"
  check_rc=$?
  if (( check_rc != 0 )); then
    log ERROR "operation=precommit_check rc=$check_rc output=$(printf '%s' "$check_output" | compact) action=manual_review"
    exit 32
  fi
  commit_output="$($GIT_BIN -C "$VAULT" commit -m "auto-sync [$HOST_TAG]" 2>&1)"
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

ahead="$($GIT_BIN -C "$VAULT" rev-list --count origin/main..HEAD 2>/dev/null || printf '0')"
if [[ "$ahead" != "0" ]]; then
  if ! run_with_retry push "$GIT_BIN" -C "$VAULT" push origin main; then
    # One final rebase+push cycle for a non-fast-forward race.
    log WARN "operation=push retry_after_pull=true"
    if ! pull_latest || ! run_with_retry push-final "$GIT_BIN" -C "$VAULT" push origin main; then
      log ERROR "operation=push result=failed action=manual_review"
      exit 35
    fi
  fi
fi

counts="$(repo_counts)"
if [[ "$counts" == "dirty=0 ahead=0 behind=0" ]]; then
  log OK "mode=sync committed=$committed pushed=$([[ "$ahead" != "0" ]] && printf 1 || printf 0) $counts"
  exit 0
fi

log WARN "mode=sync committed=$committed $counts action=inspect"
exit 36
