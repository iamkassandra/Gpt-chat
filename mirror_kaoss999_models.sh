#!/usr/bin/env bash
set -euo pipefail

REPO_LIST="${1:-KAOSS999_REPOS.txt}"
OUT_DIR="${2:-Kaoss999_models_full}"

mkdir -p "$OUT_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required" >&2
  exit 1
fi

if ! command -v git-lfs >/dev/null 2>&1; then
  echo "git-lfs is required (install git lfs first)" >&2
  exit 1
fi

while IFS= read -r repo || [[ -n "$repo" ]]; do
  [[ -z "$repo" ]] && continue
  target="$OUT_DIR/${repo//\//__}"
  if [[ -d "$target/.git" ]]; then
    echo "[skip] $repo already cloned"
    continue
  fi

  echo "[clone] $repo"
  git clone "https://huggingface.co/$repo" "$target"
  (
    cd "$target"
    git lfs fetch --all || true
    git lfs checkout || true
  )
done < "$REPO_LIST"

echo "Done. Mirrored repos in: $OUT_DIR"
