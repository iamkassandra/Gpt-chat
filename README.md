# Gpt-chat

This repo is configured to mirror **all Kaoss999 Hugging Face repos** directly into this GitHub repository.

## What is now configured

- `KAOSS999_REPOS.txt` → full list of 100 repos to mirror.
- `scripts/mirror_to_github_branches.sh` → mirrors each HF repo to a branch in this GitHub repo.
- `.github/workflows/kaoss999-auto-sync.yml` → scheduled/manual workflow that executes full mirroring.

## Output layout in GitHub

Each HF repo is pushed to its own branch:

- `hf-kaoss999/Cowgirl`
- `hf-kaoss999/Cowgirl1`
- ...

This keeps all repositories separated and avoids overwriting one another.

## Run it now

1. Push this branch to GitHub.
2. Open **Actions → Kaoss999 Full Mirror To GitHub**.
3. Click **Run workflow**.
4. Optional inputs:
   - `branch_prefix` (default: `hf-kaoss999`)
   - `max_retries` (default: `3`)

Nightly auto-run is enabled at `03:00 UTC`.

## Notes

- The workflow uses `github.token` to push branches back into this same repository.
- Git LFS payload transfer is attempted for every mirrored repo (`git lfs fetch --all` + `git lfs push --all`).
- If your GitHub LFS quota is exceeded, the workflow will fail on payload upload for affected repos.
