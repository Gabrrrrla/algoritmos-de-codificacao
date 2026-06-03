"""
Input validation functions.
"""

from typing import Dict, List, Tuple


def validate_binary_string(binary: str) -> str:
    """
    Valida string binária: remove espaços, exige somente '0' e '1'.

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


def parse_binary_input(raw: str) -> Tuple[str, List[str]]:
    """Aceita string binária pura ou texto arbitrário.

    Se a entrada (sem espaços) for composta apenas de '0' e '1', é usada
    diretamente. Caso contrário, cada caractere é convertido para seu valor
    Unicode e representado em binário (8 bits para ASCII, largura mínima para
    codepoints maiores).

    Returns:
        (binary, ascii_lines) onde ascii_lines é uma lista de strings de
        mapeamento legíveis ("'b' = 98 → 01100010") — vazia se a entrada já
        era binária.
    """
    if not isinstance(raw, str):
        raise TypeError("A entrada deve ser uma string.")
    stripped = raw.replace(" ", "")
    if not stripped:
        raise ValueError("A entrada não pode estar vazia.")
    if all(b in "01" for b in stripped):
        return stripped, []

    ascii_lines: List[str] = []
    bits: List[str] = []
    for char in raw:
        code = ord(char)
        width = 8 if code < 256 else code.bit_length()
        b = format(code, f"0{width}b")
        ascii_lines.append(f"'{char}' = {code} → {b}")
        bits.append(b)
    return "".join(bits), ascii_lines


def validate_binary_string(binary: str) -> str:
    """
    Valida string binária: remove espaços, exige somente '0' e '1'.

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


def validate_text(text: str, min_length: int = 1) -> str:
    """
    Valida entrada de texto.

    Raises:
        TypeError: Se não for string.
        ValueError: Se for mais curta que min_length.
    """
    if not isinstance(text, str):
        raise TypeError(f"Text must be a string, got {type(text).__name__}")
    if len(text) < min_length:
        raise ValueError(f"Text must be at least {min_length} characters, got {len(text)}")
    return text


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
