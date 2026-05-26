"""
Testes unitários para CRC-4 (polinômio 10011).

Cobre:
  - Cálculo do checksum (bits CRC)
  - Transmissão (mensagem + CRC)
  - Verificação sem erro (resto == 0)
  - Verificação com erro (resto != 0)
  - Roundtrip encode → check
  - Validações de entrada
"""

import pytest
from src.encoders.crc import (
    encode,
    check,
    CRCEncodeResult,
    CRCCheckResult,
    GENERATOR,
    _xor_divide,
)



class TestXorDivide:
    def test_zero_remainder(self):
        assert _xor_divide("10011" + "0000", "10011") == "0000"

    def test_known_remainder(self):
        remainder = _xor_divide("110100001101" + "0000", "10011")
        assert len(remainder) == 4
        assert all(b in "01" for b in remainder)



class TestEncode:
    def test_returns_crc_encode_result(self):
        assert isinstance(encode("1101"), CRCEncodeResult)

    def test_crc_length_is_4(self):
        for msg in ["1", "10110", "11001011"]:
            result = encode(msg)
            assert len(result.crc_bits) == 4

    def test_transmitted_is_message_plus_crc(self):
        result = encode("1101")
        assert result.transmitted == result.message + result.crc_bits

    def test_known_value_110100001101(self):
        result = encode("110100001101")
        assert result.crc_bits == "0011"
        assert result.transmitted == "1101000011010011"

    def test_known_value_10110(self):
        result = encode("10110")
        assert result.transmitted.startswith("10110")
        assert len(result.crc_bits) == 4

    def test_generator_stored(self):
        result = encode("1010")
        assert result.generator == GENERATOR

    def test_all_zeros_message(self):
        result = encode("0000")
        assert result.crc_bits == "0000"

    def test_strips_spaces(self):
        result = encode("1 1 0 1")
        assert result.message == "1101"



class TestCheckNoError:
    def test_returns_crc_check_result(self):
        transmitted = encode("1101").transmitted
        assert isinstance(check(transmitted), CRCCheckResult)

    def test_remainder_is_zero_when_no_error(self):
        transmitted = encode("110100001101").transmitted
        result = check(transmitted)
        assert result.remainder == "0000"
        assert not result.error_detected

    def test_no_error_for_various_messages(self):
        for msg in ["1", "0101", "11001011", "10110100"]:
            transmitted = encode(msg).transmitted
            result = check(transmitted)
            assert not result.error_detected, f"False positive for message: {msg}"

    def test_message_stored(self):
        transmitted = encode("1010").transmitted
        result = check(transmitted)
        assert result.message == "Nenhum erro detectado."



def flip_bit(s: str, idx: int) -> str:
    lst = list(s)
    lst[idx] = "1" if lst[idx] == "0" else "0"
    return "".join(lst)


class TestCheckWithError:
    def test_single_bit_error_detected(self):
        transmitted = encode("110100001101").transmitted
        for idx in range(len(transmitted)):
            corrupted = flip_bit(transmitted, idx)
            result = check(corrupted)
            assert result.error_detected, (
                f"Error at bit {idx} not detected in '{corrupted}'"
            )

    def test_remainder_nonzero_on_error(self):
        transmitted = encode("1010").transmitted
        corrupted = flip_bit(transmitted, 0)
        result = check(corrupted)
        assert result.remainder != "0000"
        assert result.error_detected

    def test_error_message_contains_remainder(self):
        transmitted = encode("1010").transmitted
        corrupted = flip_bit(transmitted, 3)
        result = check(corrupted)
        assert "Erro detectado" in result.message
        assert result.remainder in result.message



class TestRoundtrip:
    @pytest.mark.parametrize("msg", [
        "0", "1", "1010", "11001011", "0000", "1111", "110100001101",
    ])
    def test_roundtrip_clean_no_error(self, msg):
        transmitted = encode(msg).transmitted
        result = check(transmitted)
        assert not result.error_detected

    def test_roundtrip_with_error_detected(self):
        msg = "10110100"
        transmitted = encode(msg).transmitted
        corrupted = flip_bit(transmitted, 5)
        result = check(corrupted)
        assert result.error_detected



class TestValidation:
    def test_encode_empty_raises(self):
        with pytest.raises(ValueError):
            encode("")

    def test_encode_non_binary_raises(self):
        with pytest.raises(ValueError):
            encode("abc")

    def test_check_empty_raises(self):
        with pytest.raises(ValueError):
            check("")

    def test_check_non_binary_raises(self):
        with pytest.raises(ValueError):
            check("xyz")

    def test_custom_generator(self):
        result = encode("1011", generator="10011")
        assert result.generator == "10011"
        assert len(result.crc_bits) == 4
