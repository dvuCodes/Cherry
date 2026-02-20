import io
import asyncio

import pytest
from fastapi import UploadFile

from backend.utils.uploads import UploadTooLargeError, read_upload_limited


def test_read_upload_limited_ok() -> None:
    upload = UploadFile(filename="a.bin", file=io.BytesIO(b"hello"))
    data = asyncio.run(read_upload_limited(upload, max_size_bytes=10))
    assert data == b"hello"


def test_read_upload_limited_too_large() -> None:
    upload = UploadFile(filename="a.bin", file=io.BytesIO(b"0123456789ABC"))
    with pytest.raises(UploadTooLargeError):
        asyncio.run(read_upload_limited(upload, max_size_bytes=8))
