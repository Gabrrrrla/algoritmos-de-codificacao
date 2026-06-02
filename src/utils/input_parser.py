from dataclasses import dataclass
import re
from typing import Iterable, List, Optional, Sequence, Union

_SIGNED_INT_RE = re.compile(r"^[+-]?\d+$")


@dataclass(frozen=True)
class TokenMetadata:
    raw: str
    kind: str
    length: int


@dataclass(frozen=True)
class InputMetadata:
    tokens: List[TokenMetadata]
    value_kinds: List[str]


@dataclass(frozen=True)
class ParsedInput:
    raw: str
    tokens: List[str]
    numbers: List[int]
    ascii_mapping: List[str]
    has_text: bool
    metadata: InputMetadata


def split_input(raw: str) -> List[str]:
    if not isinstance(raw, str):
        raise TypeError("A entrada deve ser uma string.")

    raw = raw.strip()

    if not raw:
        raise ValueError("A entrada não pode estar vazia.")

    tokens = [token for token in re.split(r"[\s,]+", raw) if token]

    if not tokens:
        raise ValueError("A entrada não contém símbolos válidos.")

    return tokens


def _validate_integer(value: int, *, positive_only: bool) -> int:
    if positive_only and value <= 0:
        raise ValueError(
            f"Valor inválido: {value}. Este algoritmo exige inteiros positivos (> 0)."
        )

    if not positive_only and value < 0:
        raise ValueError(
            f"Valor inválido: {value}. Este algoritmo exige inteiros não negativos (>= 0)."
        )

    return value


def parse_integer_algorithm_input(
    raw: Union[str, int, Sequence[int]],
    *,
    positive_only: bool = True,
) -> ParsedInput:
    if isinstance(raw, bool):
        raise TypeError("Valores booleanos não são aceitos como entrada numérica.")

    if isinstance(raw, int):
        value = _validate_integer(raw, positive_only=positive_only)

        metadata = InputMetadata(
            tokens=[TokenMetadata(raw=str(raw), kind="number", length=1)],
            value_kinds=["number"],
        )

        return ParsedInput(
            raw=str(raw),
            tokens=[str(raw)],
            numbers=[value],
            ascii_mapping=[],
            has_text=False,
            metadata=metadata,
        )

    if isinstance(raw, Sequence) and not isinstance(raw, str):
        if not raw:
            raise ValueError("A entrada não pode estar vazia.")

        numbers: List[int] = []
        token_metadata: List[TokenMetadata] = []

        for item in raw:
            if isinstance(item, bool) or not isinstance(item, int):
                raise TypeError("Todos os valores da lista devem ser inteiros.")

            value = _validate_integer(item, positive_only=positive_only)
            numbers.append(value)
            token_metadata.append(
                TokenMetadata(raw=str(value), kind="number", length=1)
            )

        metadata = InputMetadata(
            tokens=token_metadata,
            value_kinds=["number"] * len(numbers),
        )

        return ParsedInput(
            raw=" ".join(str(n) for n in numbers),
            tokens=[str(n) for n in numbers],
            numbers=numbers,
            ascii_mapping=[],
            has_text=False,
            metadata=metadata,
        )

    tokens = split_input(raw)
    numbers: List[int] = []
    ascii_mapping: List[str] = []
    token_metadata: List[TokenMetadata] = []
    value_kinds: List[str] = []
    has_text = False

    for token in tokens:
        if _SIGNED_INT_RE.fullmatch(token):
            value = int(token)
            numbers.append(_validate_integer(value, positive_only=positive_only))
            token_metadata.append(TokenMetadata(raw=token, kind="number", length=1))
            value_kinds.append("number")
            continue

        has_text = True
        token_metadata.append(TokenMetadata(raw=token, kind="text", length=len(token)))

        for char in token:
            code = ord(char)
            numbers.append(_validate_integer(code, positive_only=positive_only))
            ascii_mapping.append(f"{repr(char)} = {code}")
            value_kinds.append("char")

    if not numbers:
        raise ValueError("A entrada não gerou nenhum símbolo numérico válido.")

    metadata = InputMetadata(
        tokens=token_metadata,
        value_kinds=value_kinds,
    )

    return ParsedInput(
        raw=str(raw),
        tokens=tokens,
        numbers=numbers,
        ascii_mapping=ascii_mapping,
        has_text=has_text,
        metadata=metadata,
    )


def parse_to_numbers(
    raw: Union[str, int, Sequence[int]],
    *,
    positive_only: bool = True,
) -> List[int]:
    return parse_integer_algorithm_input(raw, positive_only=positive_only).numbers


def parse_numbers_input(
    entrada: Union[int, str, List[int]],
    *,
    positive_only: bool = True,
) -> List[int]:
    """
    Converte entrada para lista de inteiros para uso direto nos algoritmos.

    Semântica:
    - int        → lista com um elemento
    - List[int]  → validado e retornado diretamente
    - str numérica (ex: "10 20" ou "10,20") → lista de ints
    - str de texto (ex: "TP 2") → ord() de cada caractere, preservando espaços

    Args:
        entrada: Valor a converter.
        positive_only: Se True, exige inteiros > 0; caso contrário >= 0.
    """
    minimum = 1 if positive_only else 0
    label = "positivos (> 0)" if positive_only else "não negativos (>= 0)"

    def _check(n: int) -> int:
        if n < minimum:
            raise ValueError(f"Entrada contém valor inválido: {n}. Esperado inteiros {label}.")
        return n

    if isinstance(entrada, bool):
        raise TypeError("Valores booleanos não são aceitos como entrada numérica.")

    if isinstance(entrada, int):
        return [_check(entrada)]

    if isinstance(entrada, list):
        if not entrada:
            raise ValueError("A entrada não pode estar vazia.")
        return [_check(n) for n in entrada]

    if isinstance(entrada, str):
        str_limpa = entrada.replace(",", " ").strip()
        if not str_limpa:
            raise ValueError("A entrada não pode estar vazia.")
        partes = str_limpa.split()
        if partes and all(p.lstrip("+-").isdigit() for p in partes):
            return [_check(int(p)) for p in partes]
        return [_check(ord(c)) for c in entrada]

    raise TypeError("A entrada deve ser um inteiro, string ou lista de inteiros.")


def expected_decoded_length(metadata: Optional[InputMetadata]) -> int:
    if metadata is None:
        return 0

    return sum(token.length for token in metadata.tokens)


def restore_decoded_input(
    decoded_numbers: Sequence[int],
    metadata: InputMetadata,
) -> str:
    expected = expected_decoded_length(metadata)

    if len(decoded_numbers) != expected:
        raise ValueError(
            "Não foi possível reconstruir a entrada original: "
            f"a decodificação retornou {len(decoded_numbers)} valores, "
            f"mas a entrada original tinha {expected}."
        )

    restored_tokens: List[str] = []
    index = 0

    for token in metadata.tokens:
        if token.kind == "number":
            restored_tokens.append(str(decoded_numbers[index]))
            index += 1
            continue

        chars: List[str] = []

        for _ in range(token.length):
            value = decoded_numbers[index]
            index += 1

            try:
                chars.append(chr(value))
            except (TypeError, ValueError):
                chars.append(f"<{value}>")

        restored_tokens.append("".join(chars))

    return " ".join(restored_tokens)


def format_reconstructed_decoding(
    decoded_numbers: Sequence[int],
    metadata: Optional[InputMetadata],
) -> str:
    if metadata is None:
        return (
            "Entrada reconstruída : indisponível sem metadados da codificação anterior.\n"
            "Observação           : somente pelo codeword não é possível diferenciar, "
            "por exemplo, o número 97 da letra 'a'."
        )

    try:
        restored = restore_decoded_input(decoded_numbers, metadata)
    except ValueError as exc:
        return f"Entrada reconstruída : indisponível. {exc}"

    return f"Entrada reconstruída : {restored}"


def format_ascii_mapping(mapping: Iterable[str]) -> str:
    mapping = list(mapping)

    if not mapping:
        return ""

    return "Conversão ASCII/Unicode:\n" + "\n".join(mapping)


def format_input_metadata(metadata: InputMetadata) -> str:
    labels = []

    for token in metadata.tokens:
        if token.kind == "number":
            labels.append("N")
        else:
            labels.append(f"T({token.length})")

    return "Máscara da entrada : " + " ".join(labels)