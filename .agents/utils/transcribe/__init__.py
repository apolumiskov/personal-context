"""Shared OpenAI audio transcription for agent skills.

Programmatic use (add ``repo/.agents/utils`` to ``sys.path``):

    from transcribe import run_transcription
    run_transcription(audio_path, repo_root, work_dir, output=...)
"""

from .core import (
    AUDIO_EXTENSIONS,
    is_audio_file,
    read_env_file,
    resolve_openai_api_key,
    run_transcription,
    split_audio_to_chunks,
    transcribe_audio,
)

__all__ = [
    "AUDIO_EXTENSIONS",
    "is_audio_file",
    "read_env_file",
    "resolve_openai_api_key",
    "run_transcription",
    "split_audio_to_chunks",
    "transcribe_audio",
]
