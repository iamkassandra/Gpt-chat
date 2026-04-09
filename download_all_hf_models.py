#!/usr/bin/env python3
"""
Download all Hugging Face model repositories for a given account.

Usage:
  python download_all_hf_models.py --author Kaoss999 --out ./Kaoss999_models

Optional:
  export HF_TOKEN=hf_xxx  # recommended for gated/private models
"""

import argparse
import json
import os
import random
import tarfile
import time
from datetime import datetime

from huggingface_hub import HfApi, snapshot_download


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download all HF model repos for an account")
    parser.add_argument("--author", required=True, help="HF username or org name")
    parser.add_argument("--out", default=None, help="Output directory")
    parser.add_argument("--retries", type=int, default=5, help="Retries per repo")
    parser.add_argument("--sleep", type=float, default=1.0, help="Delay between repos")
    parser.add_argument("--workers", type=int, default=4, help="Max workers per snapshot download")
    parser.add_argument("--archive", action="store_true", help="Create tar.gz archive at the end")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    author = args.author
    out_dir = os.path.abspath(args.out or f"./{author}_models_full")
    os.makedirs(out_dir, exist_ok=True)

    token = os.getenv("HF_TOKEN")
    api = HfApi(token=token)

    print(f"[{datetime.now().isoformat()}] Fetching model list for {author}...")
    models = list(api.list_models(author=author, full=True))
    model_ids = sorted([m.id for m in models if m.id and m.id.startswith(f"{author}/")])

    manifest_path = os.path.join(out_dir, "manifest.json")
    manifest = {
        "author": author,
        "timestamp_start": datetime.now().isoformat(),
        "total_models": len(model_ids),
        "results": [],
    }

    print(f"Found {len(model_ids)} model repositories.")

    ok = 0
    failed = 0

    for idx, repo_id in enumerate(model_ids, start=1):
        print(f"\n[{idx}/{len(model_ids)}] {repo_id}")
        local_dir = os.path.join(out_dir, repo_id.replace("/", "__"))
        result = {
            "repo_id": repo_id,
            "local_dir": local_dir,
            "status": "pending",
            "attempts": 0,
            "error": None,
        }

        for attempt in range(1, args.retries + 1):
            result["attempts"] = attempt
            try:
                snapshot_download(
                    repo_id=repo_id,
                    repo_type="model",
                    local_dir=local_dir,
                    local_dir_use_symlinks=False,
                    resume_download=True,
                    max_workers=args.workers,
                    token=token,
                )
                result["status"] = "ok"
                result["downloaded_at"] = datetime.now().isoformat()
                ok += 1
                print("  ✅ Downloaded")
                break
            except Exception as exc:
                result["error"] = str(exc)
                if attempt < args.retries:
                    backoff = (2 ** (attempt - 1)) + random.random()
                    print(f"  ⚠️ Attempt {attempt} failed; retrying in {backoff:.1f}s")
                    time.sleep(backoff)
                else:
                    result["status"] = "failed"
                    failed += 1
                    print(f"  ❌ Failed after {args.retries} attempts: {exc}")

        manifest["results"].append(result)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        time.sleep(args.sleep)

    manifest["timestamp_end"] = datetime.now().isoformat()
    manifest["ok"] = ok
    manifest["failed"] = failed
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 72)
    print(f"Done. OK={ok} FAILED={failed}")
    print(f"Saved to: {out_dir}")
    print(f"Manifest: {manifest_path}")

    if args.archive:
        archive_name = f"{os.path.basename(out_dir.rstrip('/'))}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        archive_path = os.path.join(os.path.dirname(out_dir), archive_name)
        print(f"Creating archive: {archive_path}")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(out_dir, arcname=os.path.basename(out_dir))
        print(f"Archive created: {archive_path}")

    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
