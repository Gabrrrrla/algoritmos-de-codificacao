"""
Elias-Gamma encoding implementation.

Recebe uma lista de inteiros positivos e converte para código Elias-Gamma.
"""

from src.utils.input_parser import parse_to_numbers
from dataclasses import dataclass
from typing import List, Union


@dataclass
class EliasGammaResult:
    numbers: List[int]
    encoded: str
    total_bits: int
    rate: float


def _validate_numbers(numbers: Union[str, List[int]]) -> List[int]:
    return parse_to_numbers(numbers, positive_only=True)


def encode(numbers: Union[str, List[int]]) -> EliasGammaResult:
    """
    Encode numbers using Elias-Gamma algorithm.

    Args:
        numbers: String formatada com espaços ou Lista de inteiros a serem codificados.

    Returns:
        EliasGammaResult dataclass with all encoding information.
    """
    valid_numbers = _validate_numbers(numbers)
    parts = []

    for n in valid_numbers:
        binary_n = bin(n)[2:]
        unary_zeros = "0" * (len(binary_n) - 1)
        parts.append(unary_zeros + binary_n)

    encoded = "".join(parts)
    total_bits = len(encoded)
    rate = total_bits / len(valid_numbers)

    return EliasGammaResult(
        numbers=valid_numbers,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def format_result(result: EliasGammaResult) -> str:
    """Format an EliasGammaResult into a human-readable string."""
    return (
        f"Números originais : {result.numbers}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )