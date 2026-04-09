#!/usr/bin/env bash
set -euo pipefail

REPO_LIST="${REPO_LIST:-KAOSS999_REPOS.txt}"
HF_BASE_URL="${HF_BASE_URL:-https://huggingface.co}"
GH_REMOTE_URL="${GH_REMOTE_URL:?GH_REMOTE_URL is required}"
BRANCH_PREFIX="${BRANCH_PREFIX:-hf-kaoss999}"
WORK_ROOT="${WORK_ROOT:-/tmp/kaoss999-mirror}"
MAX_RETRIES="${MAX_RETRIES:-3}"

mkdir -p "$WORK_ROOT"
report_jsonl="$WORK_ROOT/mirror_report.jsonl"
: > "$report_jsonl"

require() {
  command -v "$1" >/dev/null 2>&1 || { echo "$1 is required" >&2; exit 1; }
}
require git
require git-lfs

ok=0
failed=0

while IFS= read -r repo || [[ -n "$repo" ]]; do
  [[ -z "$repo" ]] && continue

  short_name="${repo#*/}"
  branch_name="$BRANCH_PREFIX/$short_name"
  repo_dir="$WORK_ROOT/${repo//\//__}"

  rm -rf "$repo_dir"

  status="failed"
  error=""

  for attempt in $(seq 1 "$MAX_RETRIES"); do
    if git clone "$HF_BASE_URL/$repo" "$repo_dir"; then
      (
        cd "$repo_dir"
        git lfs fetch --all || true
        git lfs checkout || true
        git remote add github "$GH_REMOTE_URL"
        git push github "HEAD:refs/heads/$branch_name" --force
        git lfs push github --all || true
      )
      status="ok"
      error=""
      break
    else
      error="clone failed on attempt ${attempt}"
      sleep "$attempt"
    fi
  done

  if [[ "$status" == "ok" ]]; then
    ok=$((ok + 1))
  else
    failed=$((failed + 1))
  fi

  printf '{"repo":"%s","branch":"%s","status":"%s","error":"%s"}\n' \
    "$repo" "$branch_name" "$status" "$error" >> "$report_jsonl"

done < "$REPO_LIST"

summary="$WORK_ROOT/mirror_summary.json"
cat > "$summary" <<JSON
{
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "repo_list": "$REPO_LIST",
  "ok": $ok,
  "failed": $failed,
  "branch_prefix": "$BRANCH_PREFIX"
}
JSON

cat "$summary"
if [[ "$failed" -gt 0 ]]; then
  exit 2
fi
