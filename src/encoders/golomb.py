"""
Golomb encoding implementation.

Convenção adotada neste projeto:
- a entrada do Golomb deve ser composta por inteiros não negativos (>= 0);
- o algoritmo codifica o valor diretamente, sem deslocamento interno;
- portanto:
    valor_interno = n
    q = valor_interno // m
    r = valor_interno % m
"""
from src.utils.input_parser import parse_to_numbers
from dataclasses import dataclass
from typing import List, Union
import math


@dataclass
class GolombResult:
    numbers: List[int]
    m: int
    encoded_parts: List[str]
    encoded: str
    total_bits: int
    rate: float


def _validate_m(m: int) -> None:
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise ValueError("O parâmetro m do Golomb deve ser um inteiro positivo.")


def _normalize_numbers(numbers: Union[int, List[int]]) -> List[int]:
    return parse_to_numbers(numbers, positive_only=True)


def encode(numbers: Union[int, List[int]], m: int = 4) -> GolombResult:
    """
    Encode non-negative integer(s) using Golomb coding.

    Args:
        numbers: Single non-negative integer or list of non-negative integers
        m: Golomb parameter (positive integer)

    Returns:
        GolombResult dataclass with all encoding information.
    """
    _validate_m(m)
    numbers = _normalize_numbers(numbers)

    k = math.ceil(math.log2(m)) if m > 1 else 0
    c = (2 ** k) - m if m > 1 else 0

    encoded_parts = []

    for n in numbers:
        value = n
        q = value // m
        r = value % m

        unary = "1" * q + "0"

        if m == 1:
            binary = ""
        else:
            if r < c:
                binary = format(r, f"0{k-1}b") if (k - 1) > 0 else ""
            else:
                binary = format(r + c, f"0{k}b")

        encoded_parts.append(unary + binary)

    encoded = " ".join(encoded_parts)
    total_bits = sum(len(p) for p in encoded_parts)
    rate = total_bits / len(numbers)

    return GolombResult(
        numbers=numbers,
        m=m,
        encoded_parts=encoded_parts,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def format_result(result: GolombResult) -> str:
    """Format a GolombResult into a human-readable string."""
    return (
        f"Números originais : {result.numbers}\n"
        f"Parâmetro m       : {result.m}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )