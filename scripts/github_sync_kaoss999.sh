#!/usr/bin/env bash
set -euo pipefail

REPO_LIST="${REPO_LIST:-KAOSS999_REPOS.txt}"
OUT_DIR="${OUT_DIR:-mirror_out}"
HF_BASE_URL="${HF_BASE_URL:-https://huggingface.co}"

mkdir -p "$OUT_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required" >&2
  exit 1
fi

if ! command -v git-lfs >/dev/null 2>&1; then
  echo "git-lfs is required" >&2
  exit 1
fi

ok=0
fail=0
report="$OUT_DIR/sync_report.jsonl"
: > "$report"

while IFS= read -r repo || [[ -n "$repo" ]]; do
  [[ -z "$repo" ]] && continue
  target="$OUT_DIR/${repo//\//__}"

  if [[ -d "$target/.git" ]]; then
    status="skipped_existing"
    printf '{"repo":"%s","status":"%s"}\n' "$repo" "$status" >> "$report"
    continue
  fi

  if git clone "$HF_BASE_URL/$repo" "$target"; then
    (
      cd "$target"
      git lfs fetch --all || true
      git lfs checkout || true
    )
    status="ok"
    ok=$((ok + 1))
  else
    status="failed"
    fail=$((fail + 1))
  fi

  printf '{"repo":"%s","status":"%s"}\n' "$repo" "$status" >> "$report"
done < "$REPO_LIST"

summary="$OUT_DIR/sync_summary.json"
cat > "$summary" <<JSON
{
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "repo_list": "$REPO_LIST",
  "ok": $ok,
  "failed": $fail,
  "output_dir": "$OUT_DIR"
}
JSON

echo "Sync complete: ok=$ok failed=$fail"
echo "Summary: $summary"
