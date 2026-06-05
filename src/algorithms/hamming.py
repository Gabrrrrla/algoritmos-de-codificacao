#Hamming (7,4)
# teste: 1011 0110


from dataclasses import dataclass, field
from typing import List, Optional

from src.utils.validation import parse_binary_input, validate_binary_string


@dataclass
class HammingEncodeResult:
    data_bits: str # bits de entrada limpos com padding (zeros ao final)
    blocks: List[str] # lista dos blocos de 4 bits
    codewords: List[str] #lista das codewords de 7 bits
    encoded: str # codewords juntas separadas por espaço
    total_bits: int #total de bits na saída
    ascii_mapping: List[str] = field(default_factory=list) #mapeamento ascii


@dataclass
class HammingDecodeResult:
    received: str #string recebida limpa
    blocks: List[str] # bloco de 7 bits
    syndromes: List[int] # síndrome de cada bloco
    error_positions: List[Optional[int]] #posição de erro
    corrected_blocks: List[str] # blocos apos a correção
    decoded_data: str #bits de dados extraídos
    corrected_codeword: str # codewords corrigidas juntas
    error_detected: bool #qlqr sindrome


def _encode_block(d: str) -> str:
    if len(d) != 4:
        raise ValueError("Bloco de dados deve ter exatamente 4 bits.")

    d1, d2, d3, d4 = int(d[0]), int(d[1]), int(d[2]), int(d[3])

    p1 = d1 ^ d2 ^ d4 #xor
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}" # eh assim pq p1, p2 e p3 sao potencias de dois e 
# p1 verifica ultimo bit em 1, p2 segundo bit em 1, p3 terceito bit em 1


def _syndrome(cw: str) -> int: #recebe codeword possivelmente com erro e retorna numero
    if len(cw) != 7:
        raise ValueError("Codeword Hamming deve ter exatamente 7 bits.")

    c = [int(b) for b in cw]

    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]

    return s1 * 1 + s2 * 2 + s3 * 4


def _correct_block(cw: str, syn: int) -> str:
    if syn == 0:
        return cw
    lst = list(cw) # converte a string cw em lista
    idx = syn - 1 # sindrome de 1 a 7, menos 1 pra indexar na lista
    lst[idx] = "1" if lst[idx] == "0" else "0" # troca o bit
    return "".join(lst)


def _extract_data(cw: str) -> str:
    return cw[2] + cw[4] + cw[5] + cw[6] #2, 4, 5, 6 = posições dos dados d1, d2, d3, d4

# --------------------------------------------------------------------------------------------------------------------
def encode(bits: str) -> HammingEncodeResult:
    bits_clean, ascii_mapping = parse_binary_input(bits)

    if len(bits_clean) % 4 != 0: # se nao for multiplo de 4, adiciona zeros no final para ficar
        pad = 4 - (len(bits_clean) % 4)
        bits_clean = bits_clean + "0" * pad

    blocks = [bits_clean[i : i + 4] for i in range(0, len(bits_clean), 4)]
    codewords = [_encode_block(b) for b in blocks]
    encoded = " ".join(codewords)

    return HammingEncodeResult(
        data_bits=bits_clean,
        blocks=blocks,
        codewords=codewords,
        encoded=encoded,
        total_bits=sum(len(cw) for cw in codewords),
        ascii_mapping=ascii_mapping,
    )


def decode(received: str) -> HammingDecodeResult:
    received_clean = validate_binary_string(received)

    if len(received_clean) % 7 != 0:
        raise ValueError(
            f"O comprimento da string recebida ({len(received_clean)}) "
            "não é múltiplo de 7 (blocos Hamming (7,4))."
        )

    blocks = [received_clean[i : i + 7] for i in range(0, len(received_clean), 7)]

    syndromes: List[int] = []
    error_positions: List[Optional[int]] = []
    corrected_blocks: List[str] = []
    decoded_data_bits: List[str] = []

    for block in blocks:
        syn = _syndrome(block) # pra cada bloco, chama a funçao que determina a sindrome
        corrected = _correct_block(block, syn) # corrige o erro se existir
        syndromes.append(syn)
        error_positions.append(syn if syn != 0 else None)
        corrected_blocks.append(corrected)
        decoded_data_bits.append(_extract_data(corrected)) #pega os 4 bits de dados

    corrected_codeword = " ".join(corrected_blocks)
    decoded_data = "".join(decoded_data_bits)

    return HammingDecodeResult(
        received=received_clean,
        blocks=blocks,
        syndromes=syndromes,
        error_positions=error_positions,
        corrected_blocks=corrected_blocks,
        decoded_data=decoded_data,
        corrected_codeword=corrected_codeword,
        error_detected=any(s != 0 for s in syndromes),
    )


def format_encode_result(result: HammingEncodeResult) -> str:
    lines = []
    if result.ascii_mapping:
        lines.append("Conversão ASCII/Unicode:")
        for entry in result.ascii_mapping:
            lines.append(f"  {entry}")
        lines.append(f"Binário gerado    : {result.data_bits}")
        lines.append("")
    lines += [
        f"Bits de dados     : {result.data_bits}",
        f"Blocos (4 bits)   : {result.blocks}",
    ]
    for i, (blk, cw) in enumerate(zip(result.blocks, result.codewords)):
        lines.append(f"  Bloco {i+1}: {blk} → {cw}")
    lines += [
        f"Codeword gerada   : {result.encoded}",
        f"Bits totais       : {result.total_bits}",
    ]
    return "\n".join(lines)


def format_decode_result(result: HammingDecodeResult) -> str:
    lines = [
        f"Recebido          : {result.received}",
        f"Blocos (7 bits)   : {result.blocks}",
        f"Erro detectado    : {'Sim' if result.error_detected else 'Não'}",
    ]
    for i, (blk, syn, epos, corr) in enumerate(
        zip(result.blocks, result.syndromes, result.error_positions, result.corrected_blocks)
    ):
        if syn != 0:
            lines.append(
                f"  Bloco {i+1}: {blk} | síndrome={syn} | "
                f"erro pos={epos} → corrigido: {corr}"
            )
        else:
            lines.append(f"  Bloco {i+1}: {blk} | sem erro")
    if result.error_detected:
        lines.append(f"Codeword corrigida : {result.corrected_codeword}")
    lines.append(f"Dados decodificados: {result.decoded_data}")
    return "\n".join(lines)
