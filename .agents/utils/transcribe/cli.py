#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Support both `python3 cli.py` and `python3 -m transcribe` (cwd or PYTHONPATH = .agents/utils)
_UTILS_ROOT = Path(__file__).resolve().parent.parent
if str(_UTILS_ROOT) not in sys.path:
    sys.path.insert(0, str(_UTILS_ROOT))

from transcribe.core import run_transcription


def _repo_root_from_cli() -> Path:
    # .../repo/.agents/utils/transcribe/cli.py -> parents[3] == repo
    return Path(__file__).resolve().parents[3]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio with OpenAI; writes text under work-dir/tmp unless --output is set."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to audio file.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        required=True,
        help="Skill or project root: tmp/ and chunk dirs are created here.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path for transcription text.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini-transcribe",
        help="OpenAI transcription model (default: gpt-4o-mini-transcribe).",
    )
    parser.add_argument(
        "--max-upload-mb",
        type=float,
        default=24.0,
        help="Max audio size for a single upload in MB (default: 24).",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=int,
        default=600,
        help="Chunk length in seconds when splitting large files (default: 600).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = _repo_root_from_cli()
    work_dir = args.work_dir.expanduser().resolve()
    out = run_transcription(
        args.input_file,
        repo_root,
        work_dir,
        output=args.output,
        model=args.model,
        max_upload_mb=args.max_upload_mb,
        chunk_seconds=args.chunk_seconds,
    )
    print(str(out))


if __name__ == "__main__":
    main()
