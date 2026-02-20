"""
Security helpers for authentication and request classification.
"""

from __future__ import annotations

import hmac
import os
from typing import Optional

from fastapi import Request


_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def is_loopback_host(host: Optional[str]) -> bool:
    """Return True when host resolves to a loopback/local address."""
    if not host:
        return False

    normalized = host.strip().lower()
    if normalized.startswith("[") and normalized.endswith("]"):
        normalized = normalized[1:-1]

    return normalized in _LOOPBACK_HOSTS


def parse_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Extract bearer token value from Authorization header."""
    if not authorization_header:
        return None

    parts = authorization_header.strip().split(" ", 1)
    if len(parts) != 2:
        return None

    scheme, token = parts
    if scheme.lower() != "bearer":
        return None
    token = token.strip()
    return token or None


def token_is_valid(provided_token: Optional[str], expected_token: Optional[str]) -> bool:
    """Constant-time token comparison."""
    if not provided_token or not expected_token:
        return False
    return hmac.compare_digest(provided_token, expected_token)


def get_configured_api_token() -> Optional[str]:
    """Load API token from environment."""
    token = os.getenv("VOICEBOX_API_TOKEN", "").strip()
    return token or None


def get_server_bind_host(request: Request) -> Optional[str]:
    """Extract bind host from ASGI scope."""
    server = request.scope.get("server")
    if not server or len(server) < 1:
        return None
    return server[0]


def is_remote_mode_request(request: Request) -> bool:
    """
    Return True when server is bound to non-loopback host.
    """
    bind_host = get_server_bind_host(request)
    if bind_host:
        return not is_loopback_host(bind_host)

    # Fallback if server host metadata is unavailable.
    return not is_loopback_host(request.url.hostname)


def get_request_token(request: Request) -> Optional[str]:
    """Extract token from Authorization header or query string."""
    bearer_token = parse_bearer_token(request.headers.get("Authorization"))
    if bearer_token:
        return bearer_token
    query_token = request.query_params.get("access_token")
    return query_token.strip() if query_token else None


def request_has_valid_api_token(request: Request) -> bool:
    """Validate request token against configured server token."""
    return token_is_valid(get_request_token(request), get_configured_api_token())
