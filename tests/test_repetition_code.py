"""
Testes unitários para o Código de Repetição Ri.

Cobre:
  - Codificação com diferentes fatores r
  - Decodificação sem erro
  - Decodificação com erros corrigíveis
  - Decodificação com erro não-corrigível (r par, empate)
  - Roundtrip (encode → decode)
  - Validações de entrada
"""

import pytest
from src.encoders.repetition_code import (
    encode,
    decode,
    RepetitionResult,
    RepetitionDecodeResult,
)



def flip_bit(s: str, idx: int) -> str:
    lst = list(s)
    lst[idx] = "1" if lst[idx] == "0" else "0"
    return "".join(lst)



class TestEncode:
    def test_returns_repetition_result(self):
        assert isinstance(encode("1", r=3), RepetitionResult)

    def test_single_bit_one_r3(self):
        assert encode("1", r=3).encoded == "111"

    def test_single_bit_zero_r3(self):
        assert encode("0", r=3).encoded == "000"

    def test_two_bits_r3(self):
        assert encode("10", r=3).encoded == "111000"

    def test_r1_identity(self):
        assert encode("1011", r=1).encoded == "1011"

    def test_r2(self):
        assert encode("10", r=2).encoded == "1100"

    def test_r5(self):
        assert encode("1", r=5).encoded == "11111"

    def test_total_bits(self):
        result = encode("1011", r=3)
        assert result.total_bits == 12

    def test_original_bits_preserved(self):
        result = encode("1010", r=3)
        assert result.original_bits == "1010"
        assert result.r == 3

    def test_strips_spaces(self):
        result = encode("1 0 1", r=3)
        assert result.encoded == "111000111"



class TestDecodeNoError:
    def test_returns_decode_result(self):
        assert isinstance(decode("111", r=3), RepetitionDecodeResult)

    def test_single_block_one(self):
        assert decode("111", r=3).decoded_bits == "1"

    def test_single_block_zero(self):
        assert decode("000", r=3).decoded_bits == "0"

    def test_two_blocks(self):
        result = decode("111000", r=3)
        assert result.decoded_bits == "10"
        assert not result.error_detected

    def test_r1_identity(self):
        assert decode("1011", r=1).decoded_bits == "1011"

    def test_r5_no_error(self):
        result = decode("11111" "00000", r=5)
        assert result.decoded_bits == "10"
        assert not result.error_detected



class TestDecodeCorrectableErrors:
    def test_single_flipped_bit_in_block_r3(self):
        corrupted = "110"
        result = decode(corrupted, r=3)
        assert result.decoded_bits == "1"
        assert result.error_detected
        assert 0 in result.error_positions

    def test_corrected_received_r3(self):
        corrupted = "001"
        result = decode(corrupted, r=3)
        assert result.decoded_bits == "0"
        assert result.corrected_received == "000"

    def test_two_blocks_one_error_each_r5(self):
        block1 = "11011"
        block2 = "00100"
        result = decode(block1 + block2, r=5)
        assert result.decoded_bits == "10"
        assert result.error_detected

    def test_errors_corrected_list_populated(self):
        result = decode("110" "001", r=3)
        assert len(result.errors_corrected) == 2

    def test_no_false_positive_on_clean_input(self):
        result = decode("111" "000" "111", r=3)
        assert not result.error_detected
        assert result.errors_corrected == []



class TestDecodeTie:
    def test_tie_block_r2_detected_not_corrected(self):
        result = decode("01", r=2)
        assert result.error_detected
        assert 0 in result.errors_detected

    def test_tie_block_r4(self):
        result = decode("1100", r=4)
        assert result.error_detected
        assert 0 in result.errors_detected



class TestRoundtrip:
    @pytest.mark.parametrize("r", [1, 3, 5, 7])
    def test_roundtrip_no_error(self, r):
        for bits in ["0", "1", "1010", "11001010"]:
            result = encode(bits, r=r)
            decoded = decode(result.encoded, r=r)
            assert decoded.decoded_bits == bits

    def test_roundtrip_with_one_error_r3(self):
        original = "1101"
        encoded = encode(original, r=3).encoded
        corrupted = flip_bit(encoded, 1)
        result = decode(corrupted, r=3)
        assert result.decoded_bits == original

    def test_roundtrip_with_one_error_r5(self):
        original = "101"
        encoded = encode(original, r=5).encoded
        corrupted = flip_bit(encoded, 2)
        result = decode(corrupted, r=5)
        assert result.decoded_bits == original



class TestValidation:
    def test_encode_empty_raises(self):
        with pytest.raises(ValueError):
            encode("", r=3)

    def test_encode_non_binary_raises(self):
        with pytest.raises(ValueError):
            encode("abc", r=3)

    def test_encode_r_zero_raises(self):
        with pytest.raises(ValueError):
            encode("1", r=0)

    def test_encode_r_negative_raises(self):
        with pytest.raises(ValueError):
            encode("1", r=-1)

    def test_decode_length_not_multiple_of_r_raises(self):
        with pytest.raises(ValueError):
            decode("1101", r=3)

    def test_decode_empty_raises(self):
        with pytest.raises(ValueError):
            decode("", r=3)

    def test_decode_non_binary_raises(self):
        with pytest.raises(ValueError):
            decode("xyz", r=3)
