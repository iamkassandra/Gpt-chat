# Gpt-chat

This repo is configured to mirror **all current Kaoss999 Hugging Face model repos** directly into this GitHub repository.

## What is configured

- `scripts/export_hf_model_list.py` → fetches the *live* model-repo list from Hugging Face for an account.
- `scripts/mirror_to_github_branches.sh` → clones each HF repo, pulls LFS payloads, and mirrors it to a branch in this GitHub repo.
- `.github/workflows/kaoss999-auto-sync.yml` → scheduled/manual workflow that runs the full export + mirror process.

## Output layout in GitHub

Each HF model repo is pushed to its own branch:

- `hf-kaoss999/Cowgirl`
- `hf-kaoss999/Cowgirl1`
- ...

This keeps repositories separated and avoids overwriting one another.

## Run it now

1. Push this branch to GitHub.
2. Open **Actions → Kaoss999 Full Mirror To GitHub**.
3. Click **Run workflow** (or let scheduled runs execute nightly at `03:00 UTC`).
4. Optional workflow inputs:
   - `branch_prefix` (default: `hf-kaoss999`)
   - `max_retries` (default: `3`)

## Important behavior

- The workflow gets the list from Hugging Face at runtime, so it is not limited to the static list file.
- Mirroring is strict: if clone/LFS fetch/LFS push fails for any repo, that repo is marked failed and the job exits non-zero.
- Reports are uploaded as workflow artifacts:
  - `repos.txt` (live list used)
  - `mirror_report.jsonl` (per-repo status)
  - `mirror_summary.json` (success/failure totals)

A mirror is only “fully complete” when workflow summary shows `failed: 0`.
