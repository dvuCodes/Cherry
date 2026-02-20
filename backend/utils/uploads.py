"""
Helpers for safe upload handling.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

from fastapi import UploadFile


class UploadTooLargeError(ValueError):
    """Raised when uploaded content exceeds configured limits."""


async def read_upload_limited(
    upload_file: UploadFile,
    max_size_bytes: int,
    chunk_size: int = 1024 * 1024,
) -> bytes:
    """Read an UploadFile with a strict maximum size."""
    total_read = 0
    chunks: list[bytes] = []

    while True:
        chunk = await upload_file.read(chunk_size)
        if not chunk:
            break

        total_read += len(chunk)
        if total_read > max_size_bytes:
            raise UploadTooLargeError(
                f"File too large. Maximum size is {max_size_bytes / (1024 * 1024):.0f}MB"
            )

        chunks.append(chunk)

    return b"".join(chunks)


async def save_upload_to_temp(
    upload_file: UploadFile,
    *,
    suffix: str,
    max_size_bytes: int,
    chunk_size: int = 1024 * 1024,
) -> Path:
    """Stream upload into a temp file while enforcing max size."""
    total_read = 0
    temp_path: Optional[Path] = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_path = Path(tmp.name)

            while True:
                chunk = await upload_file.read(chunk_size)
                if not chunk:
                    break

                total_read += len(chunk)
                if total_read > max_size_bytes:
                    raise UploadTooLargeError(
                        f"File too large. Maximum size is {max_size_bytes / (1024 * 1024):.0f}MB"
                    )

                tmp.write(chunk)

        return temp_path
    except Exception:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise
