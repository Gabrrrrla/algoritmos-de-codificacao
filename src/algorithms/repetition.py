#Repetition code (Ri)

from dataclasses import dataclass, field
from typing import List

from src.utils.validation import parse_binary_input, validate_binary_string, validate_repetition_r


@dataclass
class RepetitionResult:
    original_bits: str
    r: int
    encoded: str
    total_bits: int
    ascii_mapping: List[str] = field(default_factory=list)


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


def encode(bits: str, r: int = 3) -> RepetitionResult:
    validate_repetition_r(r)
    bits_clean, ascii_mapping = parse_binary_input(bits)

    encoded = "".join(b * r for b in bits_clean)

    return RepetitionResult(
        original_bits=bits_clean,
        r=r,
        encoded=encoded,
        total_bits=len(encoded),
        ascii_mapping=ascii_mapping,
    )


def decode(received: str, r: int = 3) -> RepetitionDecodeResult:
    validate_repetition_r(r)
    received_clean = validate_binary_string(received)

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

        if decided * r != block:
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
    lines = []
    if result.ascii_mapping:
        lines.append("Conversão ASCII/Unicode:")
        for entry in result.ascii_mapping:
            lines.append(f"  {entry}")
        lines.append(f"Binário gerado    : {result.original_bits}")
        lines.append("")
    lines += [
        f"Bits originais    : {result.original_bits}",
        f"Fator r           : {result.r}",
        f"Codeword gerada   : {result.encoded}",
        f"Bits totais       : {result.total_bits}",
    ]
    return "\n".join(lines)


def format_decode_result(result: RepetitionDecodeResult) -> str:
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
