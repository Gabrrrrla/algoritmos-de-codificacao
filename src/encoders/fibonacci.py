"""
Fibonacci (Zeckendorf) encoding implementation.

Recebe uma lista de inteiros positivos e converte para código Fibonacci.
"""
from src.utils.input_parser import parse_to_numbers
from dataclasses import dataclass
from typing import List, Union


@dataclass
class FibonacciResult:
    numbers: List[int]
    encoded: str
    total_bits: int
    rate: float


def _validate_numbers(entrada: Union[str, List[int]]) -> List[int]:
    """
    Valida e converte a entrada para uma lista de inteiros positivos.
    Se a entrada for texto (ex: "TP 2"), converte cada caractere para ASCII.
    """
    if isinstance(entrada, list):
        if any(n <= 0 for n in entrada):
            raise ValueError("Fibonacci aceita apenas inteiros positivos maiores que zero.")
        return entrada

    if isinstance(entrada, str):
        # Substitui vírgulas por espaço para padronizar a separação
        str_limpa = entrada.replace(",", " ").strip()
        
        # String contendo apenas números (ex: "10 20 30")
        if str_limpa and all(parte.isdigit() for parte in str_limpa.split()):
            numeros = [int(x) for x in str_limpa.split()]
            if any(n <= 0 for n in numeros):
                raise ValueError("Fibonacci aceita apenas inteiros positivos maiores que zero.")
            return numeros
        
        # OU string contendo texto, palavras ou frases
        # Converte automaticamente para ASCII/Unicode
        numeros = [ord(char) for char in entrada]
        if any(n <= 0 for n in numeros):
            raise ValueError("O texto contém caracteres inválidos (código ASCII <= 0).")
        return numeros

    raise TypeError("A entrada deve ser uma string ou uma lista de inteiros.")


def encode(numbers: Union[str, List[int]]) -> FibonacciResult:
    """
    Encode numbers using Fibonacci/Zeckendorf algorithm.

    Args:
        numbers: String formatada com espaços ou Lista de inteiros a serem codificados.

    Returns:
        FibonacciResult dataclass with all encoding information.
    """
    valid_numbers = _validate_numbers(numbers)
    parts = []

    for n in valid_numbers:
        # Build Fibonacci sequence F(2)=1, F(3)=2, F(4)=3, F(5)=5, ... up to n
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


def format_result(result: FibonacciResult) -> str:
    """Format a FibonacciResult into a human-readable string."""
    return (
        f"Números originais : {result.numbers}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )