"""
Testes unitários para Hamming (7,4).

Cobre:
  - Codificação de blocos de 4 bits (valores conhecidos)
  - Bits de paridade corretos
  - Decodificação sem erro
  - Decodificação com 1 erro em cada posição (1–7)
  - Múltiplos blocos
  - Padding automático
  - Roundtrip encode → decode
  - Validações de entrada
"""

import pytest
from src.algorithms.hamming import (
    encode,
    decode,
    HammingEncodeResult,
    HammingDecodeResult,
    _encode_block,
    _syndrome,
    _correct_block,
    _extract_data,
)



def flip_bit(s: str, idx: int) -> str:
    lst = list(s)
    lst[idx] = "1" if lst[idx] == "0" else "0"
    return "".join(lst)



class TestEncodeBlock:
    """Tests against manually-computed Hamming (7,4) values."""

    def test_all_zeros(self):
        assert _encode_block("0000") == "0000000"

    def test_all_ones(self):
        assert _encode_block("1111") == "1111111"

    def test_1000(self):
        assert _encode_block("1000") == "1110000"

    def test_0100(self):
        assert _encode_block("0100") == "1001100"

    def test_0010(self):
        assert _encode_block("0010") == "0101010"

    def test_0001(self):
        assert _encode_block("0001") == "1101001"

    def test_1010(self):
        assert _encode_block("1010") == "1011010"

    def test_1011(self):
        assert _encode_block("1011") == "0110011"

    def test_1101(self):
        assert _encode_block("1101") == "1010101"

    def test_1110(self):
        assert _encode_block("1110") == "0010110"



class TestSyndrome:
    def test_no_error_all_zeros(self):
        assert _syndrome("0000000") == 0

    def test_no_error_all_ones(self):
        assert _syndrome("1111111") == 0

    @pytest.mark.parametrize("pos", [1, 2, 3, 4, 5, 6, 7])
    def test_single_error_at_each_position(self, pos):
        cw = "0000000"
        corrupted = flip_bit(cw, pos - 1)
        assert _syndrome(corrupted) == pos



class TestCorrectBlock:
    def test_no_correction_when_syndrome_zero(self):
        cw = "1001011"
        assert _correct_block(cw, 0) == cw

    @pytest.mark.parametrize("pos", [1, 2, 3, 4, 5, 6, 7])
    def test_corrects_single_error(self, pos):
        original = _encode_block("1011")
        corrupted = flip_bit(original, pos - 1)
        syn = _syndrome(corrupted)
        corrected = _correct_block(corrupted, syn)
        assert corrected == original



class TestExtractData:
    def test_extracts_positions_3_5_6_7(self):
        cw = "abcdefg"
        assert _extract_data(cw) == "cefg"

    def test_extract_from_known_codeword(self):
        cw = _encode_block("1011")
        assert _extract_data(cw) == "1011"



class TestEncode:
    def test_returns_hamming_encode_result(self):
        assert isinstance(encode("1011"), HammingEncodeResult)

    def test_single_block(self):
        result = encode("1011")
        assert result.blocks == ["1011"]
        assert result.codewords == ["0110011"]
        assert result.encoded == "0110011"

    def test_two_blocks(self):
        result = encode("10111010")
        assert len(result.blocks) == 2
        assert len(result.codewords) == 2
        assert result.total_bits == 14

    def test_padding_added_when_not_multiple_of_4(self):
        result = encode("101")
        assert result.data_bits == "1010"

    def test_total_bits_is_7_per_block(self):
        for n_blocks in [1, 2, 3, 4]:
            result = encode("0000" * n_blocks)
            assert result.total_bits == 7 * n_blocks



class TestDecode:
    def test_returns_hamming_decode_result(self):
        assert isinstance(decode("0000000"), HammingDecodeResult)

    def test_no_error_single_block(self):
        cw = _encode_block("1011")
        result = decode(cw)
        assert not result.error_detected
        assert result.decoded_data == "1011"

    def test_single_error_detected_and_corrected(self):
        original = _encode_block("1101")
        corrupted = flip_bit(original, 3)
        result = decode(corrupted)
        assert result.error_detected
        assert result.decoded_data == "1101"

    @pytest.mark.parametrize("pos", [1, 2, 3, 4, 5, 6, 7])
    def test_corrects_error_at_every_position(self, pos):
        original = _encode_block("1010")
        corrupted = flip_bit(original, pos - 1)
        result = decode(corrupted)
        assert result.decoded_data == "1010", f"Failed at error position {pos}"

    def test_two_blocks_no_error(self):
        cw = _encode_block("1011") + _encode_block("0101")
        result = decode(cw)
        assert not result.error_detected
        assert result.decoded_data == "10110101"

    def test_two_blocks_one_error_each(self):
        cw1 = flip_bit(_encode_block("1011"), 0)
        cw2 = flip_bit(_encode_block("0101"), 5)
        result = decode(cw1 + cw2)
        assert result.error_detected
        assert result.decoded_data == "10110101"

    def test_length_not_multiple_of_7_raises(self):
        with pytest.raises(ValueError):
            decode("100101")

    def test_error_positions_list_length(self):
        cw = flip_bit(_encode_block("0000"), 2)
        result = decode(cw)
        assert len(result.error_positions) == 1
        assert result.error_positions[0] is not None



class TestRoundtrip:
    @pytest.mark.parametrize("data", [
        "0000", "1111", "1010", "0101", "1001", "1100", "0110", "0011",
        "10111010", "000011110101",
    ])
    def test_roundtrip_no_error(self, data):
        encoded = encode(data)
        decoded = decode(encoded.encoded.replace(" ", ""))
        assert decoded.decoded_data == data

    @pytest.mark.parametrize("pos", [0, 1, 2, 3, 4, 5, 6])
    def test_roundtrip_with_single_error(self, pos):
        data = "1011"
        enc = encode(data).encoded.replace(" ", "")
        corrupted = flip_bit(enc, pos)
        result = decode(corrupted)
        assert result.decoded_data == data



class TestValidation:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            encode("")

    def test_non_binary_encode_raises(self):
        with pytest.raises(ValueError):
            encode("102a")

    def test_empty_decode_raises(self):
        with pytest.raises(ValueError):
            decode("")

    def test_non_binary_decode_raises(self):
        with pytest.raises(ValueError):
            decode("abc1011")
