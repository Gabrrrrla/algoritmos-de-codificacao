"""
Golomb decoding implementation.

Convenção adotada neste projeto:
- o código Golomb representa inteiros não negativos (>= 0);
- internamente a codificação é feita sobre o valor direto;
- portanto, ao decodificar:
    valor_interno = q * m + r
    n = valor_interno
"""

import math
from dataclasses import dataclass
from typing import List

from src.utils.validation import validate_golomb_m, validate_binary_string_decoder


@dataclass
class GolombDecodeResult:
    binary: str
    m: int
    numbers: List[int]
    total_bits: int


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
        # Lê a parte unária: sequência de 1s até encontrar 0.
        q = 0
        while i < len(binary) and binary[i] == "1":
            q += 1
            i += 1

        if i >= len(binary):
            raise ValueError("Sequência binária inválida (falta bit de parada do unário).")

        # Consome o zero final do unário.
        i += 1

        # Caso especial: m = 1 => não há parte do resto.
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

        value = q * m + r

        n = value
        decoded_numbers.append(n)

    return GolombDecodeResult(
        binary=binary,
        m=m,
        numbers=decoded_numbers,
        total_bits=len(binary),
    )


def format_result(result: GolombDecodeResult) -> str:
    """Format a GolombDecodeResult into a human-readable string."""
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Parâmetro m           : {result.m}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )
