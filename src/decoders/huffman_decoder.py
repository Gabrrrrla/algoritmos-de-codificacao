"""
Huffman decoding implementation.

Recebe uma string binária e uma tabela de códigos {char: código}.
Inverte a tabela e decodifica bit a bit.
"""

from dataclasses import dataclass
from typing import Dict
import json
from typing import Tuple

from src.utils.validation import validate_binary_string_decoder, validate_huffman_codes


@dataclass
class HuffmanDecodeResult:
    binary: str
    codes: Dict[str, str]
    text: str
    total_bits: int


def decode(binary: str, codes: Dict[str, str]) -> HuffmanDecodeResult:
    """
    Decode Huffman encoded binary string.

    Args:
        binary: Binary string to decode
        codes: Code table mapping characters to their binary codes

    Returns:
        HuffmanDecodeResult dataclass with decoded text and metadata.
    """
    binary = validate_binary_string_decoder(binary)
    codes = validate_huffman_codes(codes)

    # Inverte: código -> caractere
    inv = {code: char for char, code in codes.items()}

    decoded_chars = []
    buffer = ""

    for bit in binary:
        buffer += bit
        if buffer in inv:
            decoded_chars.append(inv[buffer])
            buffer = ""

    if buffer:
        raise ValueError(
            f"Sequência binária inválida: sobrou '{buffer}' sem correspondência."
        )

    text = "".join(decoded_chars)

    return HuffmanDecodeResult(
        binary=binary,
        codes=codes,
        text=text,
        total_bits=len(binary),
    )


def format_result(result: HuffmanDecodeResult) -> str:
    """Format a HuffmanDecodeResult into a human-readable string."""
    return (
        f"Binário recebido : {result.binary}\n"
        f"Tabela de códigos: {result.codes}\n"
        f"Texto decodificado: {result.text}\n"
        f"Bits processados : {result.total_bits}"
    )


def parse_from_socket(payload: str) -> Tuple[Dict[str, str], str]:
    """
    Desempacota os dados recebidos do Socket.
    Retorna a tabela de códigos e a mensagem binária.
    """
    try:
        # Divide a string em duas partes usando o primeiro '|' encontrado
        table_json, encoded = payload.split('|', 1)
        code_table = json.loads(table_json)
        return code_table, encoded
    except ValueError:
        raise ValueError("Payload inválido. Formato esperado: TABELA_JSON|MENSAGEM_BINARIA")
