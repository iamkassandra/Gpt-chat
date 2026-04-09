# Gpt-chat

Automation for mirroring Kaoss999 Hugging Face model repos, including a GitHub Actions auto-sync workflow.

## Files

- `KAOSS999_REPOS.txt`: explicit list of 100 repos.
- `mirror_kaoss999_models.sh`: local script to clone all repos and fetch LFS payloads.
- `download_all_hf_models.py`: API-based downloader (requires `huggingface_hub`).
- `scripts/github_sync_kaoss999.sh`: CI-friendly sync script used by GitHub Actions.
- `.github/workflows/kaoss999-auto-sync.yml`: scheduled + manual auto-sync workflow.

## Local one-command mirror

```bash
bash mirror_kaoss999_models.sh KAOSS999_REPOS.txt ./Kaoss999_models_full
```

## GitHub auto-pull setup (what you asked for)

1. Push this branch to GitHub.
2. In GitHub repo settings, enable GitHub Actions.
3. Run **Actions → Kaoss999 Auto Sync → Run workflow**.
4. Optional inputs:
   - `include_lfs_payloads=true` to fetch full LFS model files.
   - `push_mirror_branch=true` to push results into branch `kaoss999-mirror` under `hf-mirror/`.

The workflow also runs nightly at `03:00 UTC`.

## Important limits

- Full model payloads may exceed normal GitHub repository size limits.
- If that happens, keep `push_mirror_branch=false` and use workflow artifacts / external storage.
