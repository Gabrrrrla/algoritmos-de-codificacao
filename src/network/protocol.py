"""
Socket protocol: serialization helpers and shared constants.

Request  (client → server):
    { "algorithm": str, "codeword": str, "metadata": dict }

Response (server → client):
    { "error_detected": bool, "corrected_codeword": str,
      "error_position": int | null, "message": str }
"""

import json

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000
_BUFFER = 65535


def encode_request(algorithm: str, codeword: str, metadata: dict | None = None) -> bytes:
    payload = {
        "algorithm": algorithm,
        "codeword": codeword,
        "metadata": metadata or {},
    }
    return json.dumps(payload).encode("utf-8")


def decode_request(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


def encode_response(
    error_detected: bool,
    corrected_codeword: str,
    error_position: int | None = None,
    message: str = "",
) -> bytes:
    payload = {
        "error_detected": error_detected,
        "corrected_codeword": corrected_codeword,
        "error_position": error_position,
        "message": message,
    }
    return json.dumps(payload).encode("utf-8")


def decode_response(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


_PING = b'{"type":"ping"}'
_PONG = b'{"type":"pong"}'


def encode_ping() -> bytes:
    return _PING


def is_pong(data: bytes) -> bool:
    try:
        return json.loads(data).get("type") == "pong"
    except Exception:
        return False

