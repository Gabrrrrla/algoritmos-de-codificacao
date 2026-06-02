"""
Parser para entrada de decodificação Huffman.

Formato aceito:
    <binario> <simbolo>:<codigo>, <simbolo>:<codigo>, ...

Exemplo:
    1001011110100110 !:00, a:01, Á:100, g:101, @:110, u:111

Também aceita sem vírgulas:
    1001011110100110 !:00 a:01 Á:100 g:101 @:110 u:111

Para representar espaço como símbolo, use:
    <space>:101
    space:101
    \\s:101
"""

from typing import Dict, Tuple

from src.utils.validation import validate_binary_string


_SPACE_ALIASES = {"<space>", "space", "\\s"}


def _normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip()

    if not symbol:
        raise ValueError("Símbolo vazio na tabela de Huffman.")

    if symbol in _SPACE_ALIASES:
        return " "

    return symbol


def _validate_code(symbol: str, code: str) -> str:
    code = code.strip().rstrip(",")

    if not code:
        raise ValueError(f"Código vazio para o símbolo {symbol!r}.")

    if any(bit not in "01" for bit in code):
        raise ValueError(
            f"Código inválido para {symbol!r}: {code!r} — use apenas 0 e 1."
        )

    return code


def parse_huffman_decode_input(raw: str) -> Tuple[str, Dict[str, str]]:
    if not isinstance(raw, str):
        raise TypeError("A entrada deve ser uma string.")

    raw = raw.strip()

    if not raw:
        raise ValueError("A entrada não pode estar vazia.")

    parts = raw.split(maxsplit=1)

    if len(parts) != 2:
        raise ValueError(
            "Para decodificar Huffman, informe o binário e a tabela de códigos.\n"
            "Exemplo: 100101 !:00, a:01, b:10"
        )

    binary = validate_binary_string(parts[0])
    table_raw = parts[1].strip()

    if not table_raw:
        raise ValueError("Tabela de códigos Huffman não informada.")

    codes: Dict[str, str] = {}

    if "," in table_raw:
        pairs = [part.strip() for part in table_raw.split(",") if part.strip()]
    else:
        pairs = [part.strip() for part in table_raw.split() if part.strip()]

    for pair in pairs:
        if ":" not in pair:
            raise ValueError(
                f"Par inválido na tabela Huffman: {pair!r}. "
                "Use o formato símbolo:código."
            )

        symbol_raw, code_raw = pair.split(":", 1)

        symbol = _normalize_symbol(symbol_raw)
        code = _validate_code(symbol, code_raw)

        if symbol in codes:
            raise ValueError(f"Símbolo duplicado na tabela Huffman: {symbol!r}.")

        if code in codes.values():
            raise ValueError(f"Código duplicado na tabela Huffman: {code!r}.")

        codes[symbol] = code

    if not codes:
        raise ValueError("Tabela de códigos Huffman vazia.")

    return binary, codes