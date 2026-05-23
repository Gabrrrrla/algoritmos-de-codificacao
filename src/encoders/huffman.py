"""
Huffman encoding implementation.

Fluxo:
  1. Calcular frequência de cada caractere do texto
  2. Construir a árvore de Huffman (min-heap)
  3. Gerar a tabela de códigos (percorrer árvore)
  4. Codificar o texto usando a tabela
"""

import heapq
import json
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


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


def _validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("A entrada deve ser uma string.")
    if not text:
        raise ValueError("O texto não pode estar vazio.")
    return text


def build_frequency_table(text: str) -> Dict[str, int]:
    """Retorna dicionário {caractere: frequência}."""
    return dict(Counter(text))


def build_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    """
    Constrói a árvore de Huffman a partir da tabela de frequências.

    Retorna o nó raiz.
    """
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
    """
    Percorre a árvore e gera {caractere: código_binário}.
    Esquerda = '0', Direita = '1'.
    """
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
        text: Text string to encode

    Returns:
        HuffmanResult dataclass with all encoding information.
    """
    text = _validate_text(text)

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


def format_result(result: HuffmanResult) -> str:
    """Format a HuffmanResult into a human-readable string."""
    return (
        f"Texto original : {result.text}\n"
        f"Frequências    : {result.freq_table}\n"
        f"Tabela de codes: {result.code_table}\n"
        f"Binário        : {result.encoded}\n"
        f"Bits totais    : {result.total_bits}\n"
        f"Taxa           : {result.rate:.2f} bits/símbolo"
    )


def format_for_socket(result: HuffmanResult) -> str:
    """
    Empacota a tabela e a mensagem em uma única string para envio via Socket.
    Formato: JSON_DA_TABELA|MENSAGEM_BINARIA
    """
    # json.dumps converte o dicionário python para uma string JSON
    table_json = json.dumps(result.code_table)
    return f"{table_json}|{result.encoded}"