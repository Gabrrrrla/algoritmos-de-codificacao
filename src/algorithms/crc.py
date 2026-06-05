#CRC-4

from dataclasses import dataclass, field
from typing import List, Optional

from src.utils.validation import parse_binary_input, validate_binary_string


GENERATOR = "10011"


@dataclass
class CRCEncodeResult:
    message: str
    crc_bits: str
    transmitted: str
    generator: str
    ascii_mapping: List[str] = field(default_factory=list)


@dataclass
class CRCCheckResult:
    received: str
    original_message: str
    remainder: str
    error_detected: bool
    generator: str
    message: str


def _try_decode_ascii(bits: str) -> str:
    if len(bits) % 8 != 0:
        return ""
    chars = []
    for i in range(0, len(bits), 8):
        val = int(bits[i : i + 8], 2)
        if val < 32 or val > 126:
            return ""
        chars.append(chr(val))
    return "".join(chars)


def _xor_divide(dividend: str, divisor: str) -> str:
    deg = len(divisor)
    remainder = list(dividend)

    for i in range(len(dividend) - deg + 1):
        if remainder[i] == "1":
            for j in range(deg):
                remainder[i + j] = "1" if remainder[i + j] != divisor[j] else "0"

    remainder_str = "".join(remainder[-(deg - 1):])
    return remainder_str


def encode(message: str, generator: str = GENERATOR) -> CRCEncodeResult:
    message_clean, ascii_mapping = parse_binary_input(message)
    gen_clean = validate_binary_string(generator)

    crc_len = len(gen_clean) - 1
    augmented = message_clean + "0" * crc_len
    crc_bits = _xor_divide(augmented, gen_clean)
    transmitted = message_clean + crc_bits

    return CRCEncodeResult(
        message=message_clean,
        crc_bits=crc_bits,
        transmitted=transmitted,
        generator=gen_clean,
        ascii_mapping=ascii_mapping,
    )


def check(received: str, generator: str = GENERATOR) -> CRCCheckResult:
    received_clean = validate_binary_string(received)
    gen_clean = validate_binary_string(generator)

    remainder = _xor_divide(received_clean, gen_clean)
    error = any(b == "1" for b in remainder)

    if error:
        msg = f"Erro detectado! Resto={remainder}"
    else:
        msg = "Nenhum erro detectado."

    return CRCCheckResult(
        received=received_clean,
        original_message=received_clean[: -len(gen_clean) + 1],
        remainder=remainder,
        error_detected=error,
        generator=gen_clean,
        message=msg,
    )


def format_encode_result(result: CRCEncodeResult) -> str:
    lines = []
    if result.ascii_mapping:
        lines.append("Conversão ASCII/Unicode:")
        for entry in result.ascii_mapping:
            lines.append(f"  {entry}")
        lines.append(f"Binário gerado    : {result.message}")
        lines.append("")
    lines += [
        f"Mensagem original : {result.message}",
        f"Polinômio gerador : {result.generator}",
        f"Bits CRC          : {result.crc_bits}",
        f"Transmitido       : {result.transmitted}",
    ]
    return "\n".join(lines)


def format_check_result(result: CRCCheckResult) -> str:
    decoded = _try_decode_ascii(result.original_message)
    original_line = (
        f"Mensagem original : {result.original_message} ({decoded})\n"
        if decoded
        else f"Mensagem original : {result.original_message}\n"
    )
    return (
        f"Recebido          : {result.received}\n"
        + original_line +
        f"Polinômio gerador : {result.generator}\n"
        f"Resto (remainder) : {result.remainder}\n"
        f"Erro detectado    : {'Sim' if result.error_detected else 'Não'}\n"
        f"Resultado         : {result.message}"
    )
