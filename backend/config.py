"""
Configuration module for voicebox backend.

Handles data directory configuration for production bundling.
"""

import os
from pathlib import Path
from typing import Optional

# Default data directory (used in development)
_data_dir = Path("data")


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, minimum: int = 1) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        parsed = int(value.strip())
    except (TypeError, ValueError):
        return default
    return max(minimum, parsed)

def set_data_dir(path: str | Path):
    """
    Set the data directory path.

    Args:
        path: Path to the data directory
    """
    global _data_dir
    _data_dir = Path(path)
    _data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Data directory set to: {_data_dir.absolute()}")

def get_data_dir() -> Path:
    """
    Get the data directory path.

    Returns:
        Path to the data directory
    """
    return _data_dir

def get_db_path() -> Path:
    """Get database file path."""
    return _data_dir / "voicebox.db"

def get_profiles_dir() -> Path:
    """Get profiles directory path."""
    path = _data_dir / "profiles"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_generations_dir() -> Path:
    """Get generations directory path."""
    path = _data_dir / "generations"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_cache_dir() -> Path:
    """Get cache directory path."""
    path = _data_dir / "cache"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_models_dir() -> Path:
    """Get models directory path."""
    path = _data_dir / "models"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_runtime_env() -> str:
    """Get runtime environment name."""
    return os.getenv("VOICEBOX_ENV", "development").strip().lower()


def docs_enabled() -> bool:
    """Return whether OpenAPI docs should be publicly exposed."""
    return _env_bool("VOICEBOX_ENABLE_DOCS", default=get_runtime_env() in {"dev", "development"})


def get_allowed_cors_origins() -> list[str]:
    """
    Parse explicit CORS origins from env.
    """
    raw = os.getenv("VOICEBOX_ALLOWED_ORIGINS", "")
    if raw.strip():
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    # Default explicit list for local development + Tauri.
    return [
        "http://localhost",
        "http://127.0.0.1",
        "https://localhost",
        "https://127.0.0.1",
        "tauri://localhost",
        "http://tauri.localhost",
        "https://tauri.localhost",
    ]


def get_default_cors_origin_regex() -> Optional[str]:
    """
    Localhost regex fallback only when explicit origins are not configured.
    """
    raw = os.getenv("VOICEBOX_ALLOWED_ORIGINS", "")
    if raw.strip():
        return None
    return r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"


def get_max_upload_mb_audio() -> int:
    """Maximum upload size for large audio payloads."""
    return _env_int("VOICEBOX_MAX_UPLOAD_MB_AUDIO", default=100, minimum=1)


def get_max_upload_mb_image() -> int:
    """Maximum upload size for avatar/image payloads."""
    return _env_int("VOICEBOX_MAX_UPLOAD_MB_IMAGE", default=5, minimum=1)
