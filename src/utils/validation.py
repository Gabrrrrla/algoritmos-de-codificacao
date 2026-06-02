"""
Input validation functions.
"""

from typing import Union, List, Any, Dict


def validate_positive_int(value: Any, name: str = "value") -> int:
    """
    Validate that value is a positive integer.

    Args:
        value: Value to validate
        name: Name of value for error messages

    Returns:
        Validated integer

    Raises:
        ValueError: If value is not a positive integer
        TypeError: If value is not an integer
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    
    return value


def validate_non_negative_int(value: Any, name: str = "value") -> int:
    """
    Validate that value is a non-negative integer.

    Args:
        value: Value to validate
        name: Name of value for error messages

    Returns:
        Validated integer

    Raises:
        ValueError: If value is negative
        TypeError: If value is not an integer
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    
    return value


def validate_binary_string(binary: str) -> str:
    """
    Validate that string contains only binary digits.

    Args:
        binary: String to validate

    Returns:
        Validated binary string

    Raises:
        ValueError: If string is not valid binary
        TypeError: If input is not a string
    """
    if not isinstance(binary, str):
        raise TypeError(f"Binary input must be a string, got {type(binary).__name__}")
    
    if not binary:
        raise ValueError("Binary string cannot be empty")
    
    if not all(c in '01' for c in binary):
        raise ValueError(f"Invalid binary string: contains non-binary characters")
    
    return binary


def validate_int_list(values: Any, positive_only: bool = False) -> List[int]:
    """
    Validate that values is a list of integers.

    Args:
        values: Values to validate
        positive_only: If True, all values must be positive

    Returns:
        Validated list of integers

    Raises:
        ValueError: If any value is invalid
        TypeError: If values is not a list or contains non-integers
    """
    if not isinstance(values, list):
        raise TypeError(f"Expected list, got {type(values).__name__}")
    
    if not values:
        raise ValueError("List cannot be empty")
    
    for i, value in enumerate(values):
        if not isinstance(value, int):
            raise TypeError(f"Element {i} must be an integer, got {type(value).__name__}")
        
        if positive_only and value <= 0:
            raise ValueError(f"Element {i} must be positive, got {value}")
        elif not positive_only and value < 0:
            raise ValueError(f"Element {i} must be non-negative, got {value}")
    
    return values


def validate_text(text: str, min_length: int = 1) -> str:
    """
    Validate text input.

    Args:
        text: Text to validate
        min_length: Minimum required length

    Returns:
        Validated text

    Raises:
        ValueError: If text is too short
        TypeError: If text is not a string
    """
    if not isinstance(text, str):
        raise TypeError(f"Text must be a string, got {type(text).__name__}")

    if len(text) < min_length:
        raise ValueError(f"Text must be at least {min_length} characters, got {len(text)}")

    return text


def validate_binary_string_decoder(binary: str) -> str:
    """
    Valida string binária de entrada para decoders: aceita espaços (removidos),
    exige somente '0' e '1'.

    Returns:
        String binária sem espaços.

    Raises:
        TypeError: Se a entrada não for string.
        ValueError: Se estiver vazia ou contiver caracteres inválidos.
    """
    if not isinstance(binary, str):
        raise TypeError("A entrada binária deve ser uma string.")
    binary = binary.replace(" ", "")
    if not binary:
        raise ValueError("A entrada binária não pode estar vazia.")
    if any(bit not in "01" for bit in binary):
        raise ValueError("Código binário inválido — use apenas 0 e 1.")
    return binary


def validate_golomb_m(m: int) -> None:
    """
    Valida o parâmetro m do algoritmo de Golomb.

    Raises:
        ValueError: Se m não for um inteiro positivo.
    """
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise ValueError("O parâmetro m do Golomb deve ser um inteiro positivo.")


def validate_repetition_r(r: int) -> None:
    """
    Valida o parâmetro r do código de repetição.

    Raises:
        ValueError: Se r não for um inteiro positivo (>= 1).
    """
    if not isinstance(r, int) or isinstance(r, bool) or r < 1:
        raise ValueError("O parâmetro r deve ser um inteiro positivo (>= 1).")


def validate_huffman_codes(codes: Dict[str, str]) -> Dict[str, str]:
    """
    Valida a tabela de códigos Huffman: não-vazia, apenas '0'/'1',
    e propriedade prefix-free.

    Returns:
        A própria tabela se válida.

    Raises:
        ValueError: Se a tabela for inválida.
    """
    if not isinstance(codes, dict) or not codes:
        raise ValueError("A tabela de códigos não pode estar vazia.")
    for char, code in codes.items():
        if not code or any(b not in "01" for b in code):
            raise ValueError(
                f"Código inválido para '{char}': '{code}' — use apenas 0 e 1."
            )
    sorted_codes = sorted(codes.values())
    for i in range(len(sorted_codes) - 1):
        if sorted_codes[i + 1].startswith(sorted_codes[i]):
            raise ValueError(
                f"Tabela de códigos inválida: '{sorted_codes[i]}' é prefixo de "
                f"'{sorted_codes[i + 1]}'. Huffman exige códigos livres de prefixo."
            )
    return codes


def validate_positive_numbers_input(entrada: Union[str, List[int]], algorithm: str = "O algoritmo") -> List[int]:
    """
    Valida e converte entrada para lista de inteiros positivos (> 0).
    Aceita lista de ints, string numérica separada por espaços/vírgulas,
    ou string de texto (convertida para ASCII).

    Returns:
        Lista de inteiros positivos.

    Raises:
        ValueError: Se algum número não for positivo.
        TypeError: Se o tipo da entrada for inválido.
    """
    if isinstance(entrada, list):
        if any(n <= 0 for n in entrada):
            raise ValueError(f"{algorithm} aceita apenas inteiros positivos maiores que zero.")
        return entrada

    if isinstance(entrada, str):
        str_limpa = entrada.replace(",", " ").strip()
        if str_limpa and all(parte.isdigit() for parte in str_limpa.split()):
            numeros = [int(x) for x in str_limpa.split()]
            if any(n <= 0 for n in numeros):
                raise ValueError(f"{algorithm} aceita apenas inteiros positivos maiores que zero.")
            return numeros
        numeros = [ord(char) for char in entrada]
        if any(n <= 0 for n in numeros):
            raise ValueError("O texto contém caracteres inválidos (código ASCII <= 0).")
        return numeros

    raise TypeError("A entrada deve ser uma string ou uma lista de inteiros.")


def validate_non_negative_numbers_input(entrada: Union[int, str, List[int]], algorithm: str = "O algoritmo") -> List[int]:
    """
    Valida e converte entrada para lista de inteiros não negativos (>= 0).
    Aceita int, lista de ints, string numérica separada por espaços/vírgulas,
    ou string de texto (convertida para ASCII).

    Returns:
        Lista de inteiros não negativos.

    Raises:
        ValueError: Se algum número for negativo.
        TypeError: Se o tipo da entrada for inválido.
    """
    if isinstance(entrada, int):
        if entrada < 0:
            raise ValueError(f"{algorithm} aceita apenas inteiros não negativos (>= 0).")
        return [entrada]

    if isinstance(entrada, list):
        if any(n < 0 for n in entrada):
            raise ValueError(f"{algorithm} aceita apenas inteiros não negativos (>= 0).")
        return entrada

    if isinstance(entrada, str):
        str_limpa = entrada.replace(",", " ").strip()
        if str_limpa and all(parte.isdigit() for parte in str_limpa.split()):
            numeros = [int(x) for x in str_limpa.split()]
            if any(n < 0 for n in numeros):
                raise ValueError(f"{algorithm} aceita apenas inteiros não negativos (>= 0).")
            return numeros
        numeros = [ord(char) for char in entrada]
        if any(n < 0 for n in numeros):
            raise ValueError("O texto contém caracteres inválidos.")
        return numeros

    raise TypeError("A entrada deve ser um inteiro, string ou lista de inteiros.")