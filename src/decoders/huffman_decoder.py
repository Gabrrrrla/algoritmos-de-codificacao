"""
Huffman decoding implementation.

Recebe uma string binária e uma tabela de códigos {char: código}.
Inverte a tabela e decodifica bit a bit.
"""

from dataclasses import dataclass
from typing import Dict
import json
from typing import Tuple


@dataclass
class HuffmanDecodeResult:
    binary: str
    codes: Dict[str, str]
    text: str
    total_bits: int


def _validate_binary(binary: str) -> str:
    if not isinstance(binary, str):
        raise TypeError("A entrada binária deve ser uma string.")
    binary = binary.replace(" ", "")
    if not binary:
        raise ValueError("A entrada binária não pode estar vazia.")
    if any(bit not in "01" for bit in binary):
        raise ValueError("Código binário inválido — use apenas 0 e 1.")
    return binary


def _validate_codes(codes: Dict[str, str]) -> Dict[str, str]:
    if not isinstance(codes, dict) or not codes:
        raise ValueError("A tabela de códigos não pode estar vazia.")
    for char, code in codes.items():
        if not code or any(b not in "01" for b in code):
            raise ValueError(
                f"Código inválido para '{char}': '{code}' — use apenas 0 e 1."
            )
    # Verifica que nenhum código é prefixo de outro (propriedade prefix-free).
    sorted_codes = sorted(codes.values())
    for i in range(len(sorted_codes) - 1):
        if sorted_codes[i + 1].startswith(sorted_codes[i]):
            raise ValueError(
                f"Tabela de códigos inválida: '{sorted_codes[i]}' é prefixo de "
                f"'{sorted_codes[i + 1]}'. Huffman exige códigos livres de prefixo."
            )
    return codes


def decode(binary: str, codes: Dict[str, str]) -> HuffmanDecodeResult:
    """
    Decode Huffman encoded binary string.

    Args:
        binary: Binary string to decode
        codes: Code table mapping characters to their binary codes

    Returns:
        HuffmanDecodeResult dataclass with decoded text and metadata.
    """
    binary = _validate_binary(binary)
    codes = _validate_codes(codes)

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