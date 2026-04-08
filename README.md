# Gpt-chat

This repo now includes scripts/lists to mirror Kaoss999 Hugging Face model repos.

## Files

- `KAOSS999_REPOS.txt`: explicit list of 100 repos.
- `mirror_kaoss999_models.sh`: clones all repos from the list and fetches LFS objects.
- `download_all_hf_models.py`: API-based downloader for any account (requires `huggingface_hub`).

## Fastest route for Kaoss999

```bash
bash mirror_kaoss999_models.sh KAOSS999_REPOS.txt ./Kaoss999_models_full
```

## Notes

- Hugging Face repos typically store model weights in Git LFS; `git-lfs` must be installed.
- If access is blocked (proxy/network restrictions), run the same command in an unrestricted environment.
