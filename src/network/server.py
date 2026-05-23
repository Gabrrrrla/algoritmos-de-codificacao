"""
UDP server — receives encoded codewords, applies error detection/correction,
and returns the result to the client.

Error-correction algorithms (Hamming, CRC, Repetition) will be wired into
handle_request() once implemented.
"""

import socket
from src.network.protocol import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    decode_request,
    encode_response,
)

_BUFFER = 65535
_PONG = b'{"type":"pong"}'


def handle_request(request: dict) -> dict:
    """Process a decoded request and return a response dict.

    Currently echoes the codeword back unchanged.
    Replace this body (or dispatch on request["algorithm"]) once the
    error-correction modules are ready.
    """
    codeword = request.get("codeword", "")

    return {
        "error_detected": False,
        "corrected_codeword": codeword,
        "error_position": None,
        "message": "Algoritmos de correção ainda não implementados.",
    }


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the UDP server. Blocks until interrupted."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        print(f"Servidor escutando em {host}:{port}")
        print("Pressione Ctrl+C para encerrar.\n")

        while True:
            data, addr = sock.recvfrom(_BUFFER)

            try:
                request = decode_request(data)
            except Exception:
                continue

            if request.get("type") == "ping":
                sock.sendto(_PONG, addr)
                continue

            print(f"[{addr[0]}:{addr[1]}] recebido: {len(data)} bytes")

            try:
                request = decode_request(data)
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
