
#Repetition code (Ri) encoder.

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RepetitionResult:
    original_bits: str
    r: int
    encoded: str
    total_bits: int


@dataclass
class RepetitionDecodeResult:
    received: str
    r: int
    blocks: List[str]
    decoded_bits: str
    errors_detected: List[int]
    errors_corrected: List[int]
    corrected_received: str
    error_detected: bool
    error_positions: List[int]


def _validate_r(r: int) -> None:
    if not isinstance(r, int) or isinstance(r, bool) or r < 1:
        raise ValueError("O parâmetro r deve ser um inteiro positivo (>= 1).")


def _validate_binary(bits: str) -> None:
    if not bits:
        raise ValueError("A string binária não pode estar vazia.")
    if not all(b in "01" for b in bits):
        raise ValueError("A entrada deve conter apenas '0' e '1'.")


def encode(bits: str, r: int = 3) -> RepetitionResult:
    _validate_r(r)
    bits_clean = bits.replace(" ", "")
    _validate_binary(bits_clean)

    encoded = "".join(b * r for b in bits_clean)

    return RepetitionResult(
        original_bits=bits_clean,
        r=r,
        encoded=encoded,
        total_bits=len(encoded),
    )


def decode(received: str, r: int = 3) -> RepetitionDecodeResult:
    _validate_r(r)
    received_clean = received.replace(" ", "")
    _validate_binary(received_clean)

    if len(received_clean) % r != 0:
        raise ValueError(
            f"O comprimento da string recebida ({len(received_clean)}) "
            f"não é múltiplo de r={r}."
        )

    blocks: List[str] = [
        received_clean[i : i + r] for i in range(0, len(received_clean), r)
    ]

    decoded_bits: List[str] = []
    errors_detected: List[int] = []
    errors_corrected: List[int] = []
    corrected_chars = list(received_clean)

    for block_idx, block in enumerate(blocks):
        ones = block.count("1")
        zeros = block.count("0")

        if ones > zeros:
            decided = "1"
        elif zeros > ones:
            decided = "0"
        else:
            decided = block[0]
            errors_detected.append(block_idx)

        decoded_bits.append(decided)

        if block == decided * r:
            pass
        elif decided * r != block:
            if block_idx not in errors_detected:
                errors_corrected.append(block_idx)
            base = block_idx * r
            for offset, b in enumerate(block):
                if b != decided:
                    corrected_chars[base + offset] = decided

    corrected_received = "".join(corrected_chars)

    return RepetitionDecodeResult(
        received=received_clean,
        r=r,
        blocks=blocks,
        decoded_bits="".join(decoded_bits),
        errors_detected=errors_detected,
        errors_corrected=errors_corrected,
        corrected_received=corrected_received,
        error_detected=bool(errors_detected or errors_corrected),
        error_positions=sorted(set(errors_detected + errors_corrected)),
    )


def format_encode_result(result: RepetitionResult) -> str:
    """Format a RepetitionResult into a human-readable string."""
    return (
        f"Bits originais    : {result.original_bits}\n"
        f"Fator r           : {result.r}\n"
        f"Codeword gerada   : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}"
    )


def format_decode_result(result: RepetitionDecodeResult) -> str:
    """Format a RepetitionDecodeResult into a human-readable string."""
    lines = [
        f"Recebido          : {result.received}",
        f"Fator r           : {result.r}",
        f"Blocos            : {result.blocks}",
        f"Bits decodificados: {result.decoded_bits}",
        f"Erro detectado    : {'Sim' if result.error_detected else 'Não'}",
    ]

    if result.errors_corrected:
        lines.append(f"Blocos corrigidos  : {result.errors_corrected}")
        lines.append(f"Codeword corrigida : {result.corrected_received}")

    if result.errors_detected:
        lines.append(
            f"Blocos c/ empate   : {result.errors_detected} "
            "(detectado mas não corrigível com r par)"
        )

    return "\n".join(lines)
