"""
Golomb coding.

Convenção adotada neste projeto:
- entrada composta por inteiros não negativos (>= 0);
- o algoritmo codifica o valor diretamente, sem deslocamento interno;
- portanto:
    valor_interno = n
    q = valor_interno // m
    r = valor_interno % m
"""

import math
from dataclasses import dataclass
from typing import List, Union

from src.utils.validation import (
    validate_golomb_m,
    validate_non_negative_numbers_input,
    validate_binary_string_decoder,
)


@dataclass
class GolombResult:
    numbers: List[int]
    m: int
    encoded_parts: List[str]
    encoded: str
    total_bits: int
    rate: float


@dataclass
class GolombDecodeResult:
    binary: str
    m: int
    numbers: List[int]
    total_bits: int


def encode(numbers: Union[int, str, List[int]], m: int = 4) -> GolombResult:
    """
    Encode non-negative integer(s) using Golomb coding.

    Args:
        numbers: Single non-negative integer, string, or list of non-negative integers
        m: Golomb parameter (positive integer)

    Returns:
        GolombResult dataclass with all encoding information.
    """
    validate_golomb_m(m)
    valid_numbers = validate_non_negative_numbers_input(numbers, "Golomb")

    k = math.ceil(math.log2(m)) if m > 1 else 0
    c = (2 ** k) - m if m > 1 else 0

    encoded_parts = []

    for n in valid_numbers:
        q = n // m
        r = n % m

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
    rate = total_bits / len(valid_numbers) if valid_numbers else 0.0

    return GolombResult(
        numbers=valid_numbers,
        m=m,
        encoded_parts=encoded_parts,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def decode(binary: str, m: int = 4) -> GolombDecodeResult:
    """
    Decode Golomb encoded binary string.

    Args:
        binary: Binary string to decode
        m: Golomb parameter (positive integer)

    Returns:
        GolombDecodeResult dataclass with decoded numbers and metadata.
    """
    validate_golomb_m(m)
    binary = validate_binary_string_decoder(binary)

    k = math.ceil(math.log2(m)) if m > 1 else 0
    c = (2 ** k) - m if m > 1 else 0

    decoded_numbers = []
    i = 0

    while i < len(binary):
        q = 0
        while i < len(binary) and binary[i] == "1":
            q += 1
            i += 1

        if i >= len(binary):
            raise ValueError("Sequência binária inválida (falta bit de parada do unário).")

        i += 1  # consome o zero final do unário

        if m == 1:
            r = 0
        else:
            prefix_len = k - 1

            if i + prefix_len > len(binary):
                raise ValueError("Sequência binária inválida (resto incompleto).")

            x_str = binary[i:i + prefix_len]
            x = int(x_str, 2) if prefix_len > 0 else 0
            i += prefix_len

            if x < c:
                r = x
            else:
                if i >= len(binary):
                    raise ValueError(
                        "Sequência binária inválida (falta bit adicional do resto)."
                    )
                x = (x << 1) | int(binary[i])
                i += 1
                r = x - c

        decoded_numbers.append(q * m + r)

    return GolombDecodeResult(
        binary=binary,
        m=m,
        numbers=decoded_numbers,
        total_bits=len(binary),
    )


def format_encode_result(result: GolombResult) -> str:
    return (
        f"Números originais : {result.numbers}\n"
        f"Parâmetro m       : {result.m}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )


def format_decode_result(result: GolombDecodeResult) -> str:
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Parâmetro m           : {result.m}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )


# Aliases mantidos para compatibilidade com código que usa format_result
format_result = format_encode_result
