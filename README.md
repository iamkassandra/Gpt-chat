# Gpt-chat

Utility script to download all Hugging Face model repositories for a specific account.

## Usage

```bash
python -m pip install -U huggingface_hub
export HF_TOKEN=hf_xxx  # optional but recommended
python download_all_hf_models.py --author Kaoss999 --out ./Kaoss999_models_full --archive
```

This creates:
- Downloaded repositories under the output folder
- `manifest.json` with per-repository status and errors
- Optional `.tar.gz` archive when `--archive` is set
