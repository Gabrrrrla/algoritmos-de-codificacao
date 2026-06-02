"""
Fibonacci (Zeckendorf) decoding implementation.

Recebe uma string binária e decodifica para uma lista de inteiros.
"""

from dataclasses import dataclass
from typing import List

from src.utils.validation import validate_binary_string_decoder


@dataclass
class FibonacciDecodeResult:
    binary: str
    numbers: List[int]
    total_bits: int


def decode(binary: str) -> FibonacciDecodeResult:
    """
    Decode Fibonacci encoded binary string.

    Args:
        binary: Binary string to decode.

    Returns:
        FibonacciDecodeResult dataclass with decoded numbers and metadata.
    """
    binary = validate_binary_string_decoder(binary)
    fibs = [1, 2]
    result = []
    i = 0

    while i < len(binary):
        n = 0
        fib_idx = 0
        last_bit = '0'
        terminator_found = False

        while i < len(binary):
            bit = binary[i]
            i += 1

            if bit == '1' and last_bit == '1':
                terminator_found = True
                break

            if bit == '1':
                while len(fibs) <= fib_idx:
                    fibs.append(fibs[-1] + fibs[-2])
                n += fibs[fib_idx]

            last_bit = bit
            fib_idx += 1

        if not terminator_found:
            raise ValueError("Sequência binária inválida: terminador '11' não encontrado no final.")

        result.append(n)

    return FibonacciDecodeResult(
        binary=binary,
        numbers=result,
        total_bits=len(binary),
    )


def format_result(result: FibonacciDecodeResult) -> str:
    """Format a FibonacciDecodeResult into a human-readable string."""
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )
