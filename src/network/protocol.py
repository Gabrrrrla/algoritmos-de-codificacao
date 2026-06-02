"""
Socket protocol: serialization helpers and shared constants.

Every non-ping/pong packet is framed as:
    <json_bytes> + b"|" + <crc_hex>

where <crc_hex> is the CRC-4 remainder (hex string) of the JSON bytes.
The receiver strips and verifies the CRC before parsing JSON; a non-zero
remainder causes a ValueError so the caller can discard the packet.

Request  (client → server):
    { "algorithm": str, "codeword": str, "metadata": dict }

Response (server → client):
    { "error_detected": bool, "corrected_codeword": str,
      "error_position": int | null, "message": str }
"""

import json
from src.algorithms.crc import encode as crc_encode, check as crc_check

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000

_SEP = b"|"


def _bytes_to_bits(data: bytes) -> str:
    return "".join(f"{b:08b}" for b in data)


def _frame(payload_bytes: bytes) -> bytes:
    result = crc_encode(_bytes_to_bits(payload_bytes))
    return payload_bytes + _SEP + result.crc_bits.encode("ascii")


def _unframe(data: bytes) -> bytes:
    """Strip and verify CRC frame. Raises ValueError on detected error."""
    sep_idx = data.rfind(_SEP)
    if sep_idx == -1:
        raise ValueError("Pacote malformado: separador CRC ausente.")
    payload_bytes = data[:sep_idx]
    crc_bits = data[sep_idx + 1:].decode("ascii")
    bits = _bytes_to_bits(payload_bytes)
    result = crc_check(bits + crc_bits)
    if result.error_detected:
        raise ValueError(f"Erro CRC detectado: resto={result.remainder}.")
    return payload_bytes


def encode_request(algorithm: str, codeword: str, metadata: dict | None = None) -> bytes:
    payload = {
        "algorithm": algorithm,
        "codeword": codeword,
        "metadata": metadata or {},
    }
    return _frame(json.dumps(payload).encode("utf-8"))


def decode_request(data: bytes) -> dict:
    return json.loads(_unframe(data).decode("utf-8"))


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
    return _frame(json.dumps(payload).encode("utf-8"))


def decode_response(data: bytes) -> dict:
    return json.loads(_unframe(data).decode("utf-8"))


_PING = b'{"type":"ping"}'
_PONG = b'{"type":"pong"}'


def encode_ping() -> bytes:
    return _PING


def is_pong(data: bytes) -> bool:
    try:
        return json.loads(data).get("type") == "pong"
    except Exception:
        return False
