"""
UDP server — receives encoded codewords, applies error detection/correction,
and returns the result to the client.
"""

import socket
from src.network.protocol import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    decode_request,
    encode_response,
    _PING,
)
from src.algorithms import repetition, hamming, crc

_BUFFER = 65536
_PONG = b'{"type":"pong"}'


def handle_request(request: dict) -> dict:
    """Process a decoded request and return a response dict.

    Dispatches on request["algorithm"]:
      - "Repetição Ri"  → majority-vote correction
      - "Hamming (7,4)" → syndrome correction
      - "CRC-4"         → CRC remainder check
    All others are echoed back unchanged.
    """
    algo = request.get("algorithm", "")
    codeword = request.get("codeword", "")
    metadata = request.get("metadata", {})

    try:
        if algo == "Repetição Ri":
            r = int(metadata.get("r", 3))
            result = repetition.decode(codeword, r=r)
            error_pos = result.error_positions if result.error_positions else None
            return {
                "error_detected": result.error_detected,
                "corrected_codeword": result.corrected_received,
                "error_position": error_pos,
                "message": (
                    f"Blocos corrigidos: {result.errors_corrected}"
                    if result.errors_corrected
                    else "Nenhum erro detectado."
                ),
            }

        if algo == "Hamming (7,4)":
            result = hamming.decode(codeword)
            error_pos = [p for p in result.error_positions if p is not None] or None
            return {
                "error_detected": result.error_detected,
                "corrected_codeword": result.corrected_codeword,
                "error_position": error_pos,
                "message": (
                    f"Erro(s) corrigido(s) nas posições: {error_pos}"
                    if result.error_detected
                    else "Nenhum erro detectado."
                ),
            }

        if algo == "CRC-4":
            result = crc.check(codeword)
            return {
                "error_detected": result.error_detected,
                "corrected_codeword": codeword,
                "error_position": None,
                "message": result.message,
            }

    except Exception as exc:
        return {
            "error_detected": False,
            "corrected_codeword": codeword,
            "error_position": None,
            "message": f"Erro ao processar ({algo}): {exc}",
        }

    return {
        "error_detected": False,
        "corrected_codeword": codeword,
        "error_position": None,
        "message": f"Algoritmo '{algo}' recebido (sem tratamento de erro específico).",
    }


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the UDP server. Blocks until interrupted."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        print(f"Servidor escutando em {host}:{port}")
        print("Pressione Ctrl+C para encerrar.\n")

        while True:
            data, addr = sock.recvfrom(_BUFFER)

            if data == _PING:
                sock.sendto(_PONG, addr)
                continue

            try:
                request = decode_request(data)
            except ValueError as exc:
                print(f"[{addr[0]}:{addr[1]}] pacote descartado: {exc}")
                continue
            except Exception:
                continue

            print(f"[{addr[0]}:{addr[1]}] recebido: {len(data)} bytes")

            try:
                response = handle_request(request)
                print(
                    f"  algoritmo={request.get('algorithm')}  "
                    f"codeword={request.get('codeword', '')[:40]}..."
                )
            except Exception as exc:
                response = {
                    "error_detected": False,
                    "corrected_codeword": "",
                    "error_position": None,
                    "message": f"Erro ao processar requisição: {exc}",
                }

            sock.sendto(encode_response(**response), addr)
            print(f"  resposta enviada: {response['message']}\n")
