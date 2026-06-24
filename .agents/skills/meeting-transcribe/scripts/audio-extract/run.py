#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".flv",
    ".wmv",
    ".m4v",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract audio track from a video file into meeting-transcribe/tmp."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to video or audio source file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path for extracted audio (.wav by default).",
    )
    return parser.parse_args()


def is_video_file(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS


def default_output_path(input_file: Path) -> Path:
    skill_root = Path(__file__).resolve().parents[2]
    tmp_dir = skill_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return (tmp_dir / f"{input_file.stem}.wav").resolve()


def extract_audio(input_file: Path, output_file: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_file),
    ]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("Ошибка: ffmpeg не найден. Установите ffmpeg и повторите попытку.", file=sys.stderr)
        raise SystemExit(1)
    except subprocess.CalledProcessError as err:
        print(f"Ошибка ffmpeg (код {err.returncode}).", file=sys.stderr)
        raise SystemExit(err.returncode)


def main() -> None:
    args = parse_args()
    input_file = args.input_file.expanduser().resolve()

    if not input_file.exists():
        print(f"Ошибка: файл не найден: {input_file}", file=sys.stderr)
        raise SystemExit(1)

    if not input_file.is_file():
        print(f"Ошибка: путь не является файлом: {input_file}", file=sys.stderr)
        raise SystemExit(1)

    if not is_video_file(input_file):
        print(f"Передан не видео файл, извлечение не требуется: {input_file}", file=sys.stderr)
        print(str(input_file.resolve()))
        return

    output_file = (
        args.output.expanduser().resolve()
        if args.output is not None
        else default_output_path(input_file)
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)

    extract_audio(input_file, output_file)
    print(str(output_file.resolve()))


if __name__ == "__main__":
    main()
