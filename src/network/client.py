"""
UDP client — sends an encoded codeword to the error-correction server
and returns the server's response.
"""

import socket
from src.network.protocol import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    encode_request,
    decode_response,
    encode_ping,
    is_pong,
)

_TIMEOUT = 2.0
_MAX_RETRIES = 3
_BUFFER = 65535
_PING_TIMEOUT = 0.5


def check_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> bool:
    """Return True if the server is reachable (responds to a ping within 0.5 s)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(_PING_TIMEOUT)
        try:
            sock.sendto(encode_ping(), (host, port))
            data, _ = sock.recvfrom(64)
            return is_pong(data)
        except (socket.timeout, OSError):
            return False


def send_codeword(
    algorithm: str,
    codeword: str,
    metadata: dict | None = None,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> dict:
    """Send codeword to the server and return the corrected result.

    Returns a dict with keys:
        error_detected (bool), corrected_codeword (str),
        error_position (int | None), message (str)

    Raises:
        TimeoutError  — server did not respond after MAX_RETRIES attempts
        OSError       — network-level failure
    """
    data = encode_request(algorithm, codeword, metadata)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(_TIMEOUT)

        for attempt in range(_MAX_RETRIES):
            try:
                sock.sendto(data, (host, port))
                response_data, _ = sock.recvfrom(_BUFFER)
                return decode_response(response_data)
            except socket.timeout:
                if attempt == _MAX_RETRIES - 1:
                    raise TimeoutError(
                        f"Servidor não respondeu após {_MAX_RETRIES} tentativas "
                        f"({host}:{port})."
                    )
