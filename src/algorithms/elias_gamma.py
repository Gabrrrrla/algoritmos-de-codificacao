"""
Elias-Gamma coding.

Encode: recebe inteiros positivos, converte para código Elias-Gamma.
Decode: recebe string binária, decodifica para lista de inteiros.
"""

from dataclasses import dataclass
from typing import List, Union

from src.utils.input_parser import parse_to_numbers
from src.utils.validation import (
    validate_positive_numbers_input,
    validate_binary_string_decoder,
)


@dataclass
class EliasGammaResult:
    numbers: List[int]
    encoded: str
    total_bits: int
    rate: float


@dataclass
class EliasGammaDecodeResult:
    binary: str
    numbers: List[int]
    total_bits: int


def encode(numbers: Union[str, List[int]]) -> EliasGammaResult:
    """
    Encode numbers using Elias-Gamma algorithm.

    Args:
        numbers: String formatada com espaços/vírgulas ou lista de inteiros positivos.

    Returns:
        EliasGammaResult dataclass with all encoding information.
    """
    valid_numbers = validate_positive_numbers_input(numbers, "Elias-Gamma")
    parts = []

    for n in valid_numbers:
        binary_n = bin(n)[2:]
        unary_zeros = "0" * (len(binary_n) - 1)
        parts.append(unary_zeros + binary_n)

    encoded = "".join(parts)
    total_bits = len(encoded)
    rate = total_bits / len(valid_numbers) if valid_numbers else 0.0

    return EliasGammaResult(
        numbers=valid_numbers,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


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


def format_encode_result(result: EliasGammaResult) -> str:
    return (
        f"Números originais : {result.numbers}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )


def format_decode_result(result: EliasGammaDecodeResult) -> str:
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )


# Aliases mantidos para compatibilidade com código que usa format_result
format_result = format_encode_result
