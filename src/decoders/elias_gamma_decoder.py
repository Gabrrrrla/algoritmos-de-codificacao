"""
Elias-Gamma decoding implementation.

Recebe uma string binária e decodifica para uma lista de inteiros.
"""

from dataclasses import dataclass
from typing import List

from src.utils.validation import validate_binary_string_decoder


@dataclass
class EliasGammaDecodeResult:
    binary: str
    numbers: List[int]
    total_bits: int


def decode(binary: str) -> EliasGammaDecodeResult:
    """
    Decode Elias-Gamma encoded binary string.

    Args:
        binary: Binary string to decode.

    Returns:
        EliasGammaDecodeResult dataclass with decoded numbers and metadata.
    """
    binary = validate_binary_string_decoder(binary)
    result = []
    i = 0

    while i < len(binary):
        zeros = 0
        while i < len(binary) and binary[i] == '0':
            zeros += 1
            i += 1

        if i + zeros + 1 > len(binary):
            raise ValueError(
                f"Sequência binária inválida: erro ao tentar ler os bits após {zeros} zeros."
            )

        bin_part = binary[i: i + zeros + 1]
        result.append(int(bin_part, 2))
        i += zeros + 1

    return EliasGammaDecodeResult(
        binary=binary,
        numbers=result,
        total_bits=len(binary),
    )


def format_result(result: EliasGammaDecodeResult) -> str:
    """Format an EliasGammaDecodeResult into a human-readable string."""
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )
