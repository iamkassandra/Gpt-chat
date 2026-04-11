#!/usr/bin/env python3
"""Export all model repo IDs for a Hugging Face account."""

import argparse
from pathlib import Path

from huggingface_hub import HfApi


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Hugging Face model IDs")
    parser.add_argument("--author", required=True, help="HF username/org (e.g., Kaoss999)")
    parser.add_argument("--out", required=True, help="Output text file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api = HfApi()

    model_ids = sorted(
        {
            model.id
            for model in api.list_models(author=args.author, full=False)
            if model.id and model.id.startswith(f"{args.author}/")
        }
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(model_ids) + ("\n" if model_ids else ""), encoding="utf-8")

    print(f"Exported {len(model_ids)} model repos for {args.author} -> {out_path}")
    return 0 if model_ids else 2


if __name__ == "__main__":
    raise SystemExit(main())
