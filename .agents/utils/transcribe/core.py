from __future__ import annotations

import subprocess
import sys
from pathlib import Path


AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".ogg",
    ".flac",
    ".webm",
    ".mp4",
    ".mpeg",
    ".mpga",
}


REGION_ERROR_MARKERS = (
    "unsupported_country_region_territory",
    "country",
    "region",
    "territory",
    "not supported in your location",
    "not available in your location",
)


def is_audio_file(path: Path) -> bool:
    return path.suffix.lower() in AUDIO_EXTENSIONS


def read_env_file(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        return {}

    result: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip("'").strip('"')
    return result


def resolve_openai_api_key(repo_root: Path) -> str:
    env_vars = read_env_file(repo_root / ".env")
    api_key = env_vars.get("OPENAI_API_KEY", "")
    if not api_key:
        print(
            "Ошибка: не найден OPENAI_API_KEY. Добавьте его в файл .env в корне проекта.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return api_key


def default_text_output_path(input_file: Path, work_dir: Path) -> Path:
    tmp_dir = work_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return (tmp_dir / f"{input_file.stem}.txt").resolve()


def default_chunks_dir(input_file: Path, work_dir: Path) -> Path:
    chunks_dir = work_dir / "tmp" / f"{input_file.stem}_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    return chunks_dir.resolve()


def split_audio_to_chunks(input_file: Path, chunk_seconds: int, chunks_dir: Path) -> list[Path]:
    if chunk_seconds <= 0:
        print("Ошибка: --chunk-seconds должен быть больше 0.", file=sys.stderr)
        raise SystemExit(1)

    output_pattern = chunks_dir / "chunk_%04d.wav"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-f",
        "segment",
        "-segment_time",
        str(chunk_seconds),
        "-ar",
        "16000",
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        str(output_pattern),
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Ошибка: ffmpeg не найден. Установите ffmpeg и повторите попытку.", file=sys.stderr)
        raise SystemExit(1)
    except subprocess.CalledProcessError as err:
        print(f"Ошибка ffmpeg при нарезке аудио (код {err.returncode}).", file=sys.stderr)
        raise SystemExit(err.returncode)

    chunks = sorted(chunks_dir.glob("chunk_*.wav"))
    if not chunks:
        print("Ошибка: не удалось создать чанки аудио.", file=sys.stderr)
        raise SystemExit(1)
    return [chunk.resolve() for chunk in chunks]


def transcribe_audio(input_file: Path, model: str, api_key: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        print(
            "Ошибка: библиотека openai не установлена. Установите: python3 -m pip install openai",
            file=sys.stderr,
        )
        raise SystemExit(1)

    client = OpenAI(api_key=api_key)
    try:
        with input_file.open("rb") as audio_fp:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_fp,
            )
    except Exception as err:  # noqa: BLE001 - keeps compatibility with OpenAI SDK versions
        err_text = str(err).lower()
        if any(marker in err_text for marker in REGION_ERROR_MARKERS):
            print("Switch on VPN", file=sys.stderr)
            raise SystemExit(1)
        raise

    return getattr(transcription, "text", "").strip()


def run_transcription(
    input_file: Path,
    repo_root: Path,
    work_dir: Path,
    *,
    output: Path | None = None,
    model: str = "gpt-4o-mini-transcribe",
    max_upload_mb: float = 24.0,
    chunk_seconds: int = 600,
) -> Path:
    """Transcribe audio to text; return path to written text file."""
    input_file = input_file.expanduser().resolve()

    if not input_file.exists():
        print(f"Ошибка: файл не найден: {input_file}", file=sys.stderr)
        raise SystemExit(1)

    if not input_file.is_file():
        print(f"Ошибка: путь не является файлом: {input_file}", file=sys.stderr)
        raise SystemExit(1)

    if not is_audio_file(input_file):
        print(
            "Ошибка: передан не аудио файл. Для видео сначала извлеките дорожку через audio-extract.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    work_dir = work_dir.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve()
    api_key = resolve_openai_api_key(repo_root)

    text_output = (
        output.expanduser().resolve()
        if output is not None
        else default_text_output_path(input_file, work_dir)
    )
    text_output.parent.mkdir(parents=True, exist_ok=True)

    max_upload_bytes = int(max_upload_mb * 1024 * 1024)
    input_size = input_file.stat().st_size

    text_parts: list[str] = []
    if input_size <= max_upload_bytes:
        text_parts.append(transcribe_audio(input_file, model, api_key))
    else:
        chunks_dir = default_chunks_dir(input_file, work_dir)
        chunk_paths = split_audio_to_chunks(input_file, chunk_seconds, chunks_dir)
        for chunk_path in chunk_paths:
            chunk_text = transcribe_audio(chunk_path, model, api_key)
            if chunk_text:
                text_parts.append(chunk_text)

    text = "\n\n".join(part for part in text_parts if part.strip()).strip()
    if not text:
        print("Ошибка: OpenAI вернул пустую транскрипцию.", file=sys.stderr)
        raise SystemExit(1)

    text_output.write_text(text + "\n", encoding="utf-8")
    return text_output.resolve()
