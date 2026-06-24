#!/usr/bin/env python3
"""Thin launcher: delegates to workspace `.agents/utils/transcribe/cli.py`."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parents[2]
_UTILS_CLI = _SKILL_ROOT.parent.parent / "utils" / "transcribe" / "cli.py"


def main() -> None:
    if not _UTILS_CLI.is_file():
        print(f"Ошибка: не найден общий скрипт транскрибации: {_UTILS_CLI}", file=sys.stderr)
        raise SystemExit(1)
    cmd = [
        sys.executable,
        str(_UTILS_CLI),
        "--work-dir",
        str(_SKILL_ROOT),
        *sys.argv[1:],
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
