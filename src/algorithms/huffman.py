"""
Huffman coding.

Encode: calcula frequências, constrói árvore, gera tabela e codifica o texto.
Decode: recebe string binária e tabela de códigos, decodifica bit a bit.
"""

import heapq
import json
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.utils.validation import (
    validate_text,
    validate_binary_string_decoder,
    validate_huffman_codes,
)


class HuffmanNode:
    """Nó da árvore de Huffman."""

    def __init__(self, char: Optional[str], freq: int,
                 left: Optional["HuffmanNode"] = None,
                 right: Optional["HuffmanNode"] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


@dataclass
class HuffmanResult:
    text: str
    freq_table: Dict[str, int]
    code_table: Dict[str, str]
    encoded: str
    total_bits: int
    rate: float


@dataclass
class HuffmanDecodeResult:
    binary: str
    codes: Dict[str, str]
    text: str
    total_bits: int


def build_frequency_table(text: str) -> Dict[str, int]:
    """Retorna dicionário {caractere: frequência}."""
    return dict(Counter(text))


def build_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    """Constrói a árvore de Huffman a partir da tabela de frequências."""
    if not freq_table:
        raise ValueError("Tabela de frequências vazia.")

    heap: List[HuffmanNode] = [
        HuffmanNode(char=ch, freq=f) for ch, f in freq_table.items()
    ]
    heapq.heapify(heap)

    if len(heap) == 1:
        node = heapq.heappop(heap)
        return HuffmanNode(char=None, freq=node.freq, left=node, right=None)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(
            char=None,
            freq=left.freq + right.freq,
            left=left,
            right=right,
        )
        heapq.heappush(heap, merged)

    return heap[0]


def build_code_table(root: HuffmanNode) -> Dict[str, str]:
    """Percorre a árvore e gera {caractere: código_binário}. Esquerda='0', Direita='1'."""
    codes: Dict[str, str] = {}

    def _traverse(node: Optional[HuffmanNode], prefix: str) -> None:
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = prefix if prefix else "0"
            return
        _traverse(node.left, prefix + "0")
        _traverse(node.right, prefix + "1")

    _traverse(root, "")
    return codes


def encode(text: str) -> HuffmanResult:
    """
    Encode text using Huffman coding.

    Args:
        text: Text string to encode.

    Returns:
        HuffmanResult dataclass with all encoding information.
    """
    text = validate_text(text)

    freq_table = build_frequency_table(text)
    tree = build_tree(freq_table)
    code_table = build_code_table(tree)

    encoded = "".join(code_table[ch] for ch in text)
    total_bits = len(encoded)
    rate = total_bits / len(text)

    return HuffmanResult(
        text=text,
        freq_table=freq_table,
        code_table=code_table,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def decode(binary: str, codes: Dict[str, str]) -> HuffmanDecodeResult:
    """
    Decode Huffman encoded binary string.

    Args:
        binary: Binary string to decode.
        codes: Code table mapping characters to their binary codes.

    Returns:
        HuffmanDecodeResult dataclass with decoded text and metadata.
    """
    binary = validate_binary_string_decoder(binary)
    codes = validate_huffman_codes(codes)

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


def format_encode_result(result: HuffmanResult) -> str:
    return (
        f"Texto original : {result.text}\n"
        f"Frequências    : {result.freq_table}\n"
        f"Tabela de codes: {result.code_table}\n"
        f"Binário        : {result.encoded}\n"
        f"Bits totais    : {result.total_bits}\n"
        f"Taxa           : {result.rate:.2f} bits/símbolo"
    )


def format_decode_result(result: HuffmanDecodeResult) -> str:
    return (
        f"Binário recebido : {result.binary}\n"
        f"Tabela de códigos: {result.codes}\n"
        f"Texto decodificado: {result.text}\n"
        f"Bits processados : {result.total_bits}"
    )


def format_for_socket(result: HuffmanResult) -> str:
    """Empacota tabela e mensagem para envio via Socket: JSON_DA_TABELA|MENSAGEM_BINARIA."""
    table_json = json.dumps(result.code_table)
    return f"{table_json}|{result.encoded}"


def parse_from_socket(payload: str) -> Tuple[Dict[str, str], str]:
    """Desempacota payload recebido do Socket. Retorna (tabela_de_códigos, binário)."""
    try:
        table_json, encoded = payload.split('|', 1)
        code_table = json.loads(table_json)
        return code_table, encoded
    except ValueError:
        raise ValueError("Payload inválido. Formato esperado: TABELA_JSON|MENSAGEM_BINARIA")


# Alias mantido para compatibilidade com código que usa format_result
format_result = format_encode_result
