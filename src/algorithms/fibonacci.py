"""
Fibonacci (Zeckendorf) coding.

Encode: recebe inteiros positivos, converte para código Fibonacci.
Decode: recebe string binária com terminador '11', decodifica para lista de inteiros.
"""

from dataclasses import dataclass
from typing import List, Union

from src.utils.input_parser import parse_numbers_input
from src.utils.validation import validate_binary_string


@dataclass
class FibonacciResult:
    numbers: List[int]
    encoded: str
    total_bits: int
    rate: float


@dataclass
class FibonacciDecodeResult:
    binary: str
    numbers: List[int]
    total_bits: int


def encode(numbers: Union[str, List[int]]) -> FibonacciResult:
    """
    Encode numbers using Fibonacci/Zeckendorf algorithm.

    Args:
        numbers: String formatada com espaços/vírgulas ou lista de inteiros positivos.

    Returns:
        FibonacciResult dataclass with all encoding information.
    """
    valid_numbers = parse_numbers_input(numbers, positive_only=True)
    parts = []

    for n in valid_numbers:
        fibs = []
        a, b = 1, 2
        while a <= n:
            fibs.append(a)
            a, b = b, a + b

        codeword = ["0"] * len(fibs)
        temp = n

        for i in range(len(fibs) - 1, -1, -1):
            if fibs[i] <= temp:
                codeword[i] = "1"
                temp -= fibs[i]

        codeword.append("1")
        parts.append("".join(codeword))

    encoded = "".join(parts)
    total_bits = len(encoded)
    rate = total_bits / len(valid_numbers) if valid_numbers else 0.0

    return FibonacciResult(
        numbers=valid_numbers,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def decode(binary: str) -> FibonacciDecodeResult:
    """
    Decode Fibonacci encoded binary string.

    Args:
        binary: Binary string to decode (each number terminated by '11').

    Returns:
        FibonacciDecodeResult dataclass with decoded numbers and metadata.
    """
    binary = validate_binary_string(binary)
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


def format_encode_result(result: FibonacciResult) -> str:
    return (
        f"Números originais : {result.numbers}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )


def format_decode_result(result: FibonacciDecodeResult) -> str:
    return (
        f"Binário recebido      : {result.binary}\n"
        f"Números decodificados : {result.numbers}\n"
        f"Bits processados      : {result.total_bits}"
    )


# Aliases mantidos para compatibilidade com código que usa format_result
format_result = format_encode_result
