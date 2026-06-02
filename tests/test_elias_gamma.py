"""
Testes integrados para o módulo Elias-Gamma.
"""

import pytest
from src.algorithms.elias_gamma import encode, EliasGammaResult
from src.algorithms.elias_gamma import decode, EliasGammaDecodeResult


def flip_bit(binary: str, index: int) -> str:
    bits = list(binary)
    bits[index] = "1" if bits[index] == "0" else "0"
    return "".join(bits)


class TestEncode:
    def test_returns_elias_gamma_result(self):
        assert isinstance(encode([5]), EliasGammaResult)

    def test_encoded_is_binary_string(self):
        result = encode([1, 10, 15])
        assert all(bit in "01" for bit in result.encoded)

    def test_known_values(self):
        assert encode([1]).encoded == "1"
        assert encode([2]).encoded == "010"
        assert encode([5]).encoded == "00101"
        assert encode([9]).encoded == "0001001"

    def test_result_fields(self):
        result = encode([1, 2, 3])
        assert result.numbers == [1, 2, 3]
        assert result.total_bits == len(result.encoded)
        assert result.rate > 0

class TestTextSupport:
    """Valida os requisitos de entrada de texto e múltiplas entradas"""
    
    def test_encode_string_of_numbers(self):
        """Testa entrada múltipla separada por espaço."""
        result = encode("10 20 30")
        assert result.numbers == [10, 20, 30]
        
    def test_encode_string_of_numbers_with_comma(self):
        """Testa entrada múltipla separada por vírgula."""
        result = encode("10, 20, 30")
        assert result.numbers == [10, 20, 30]

    def test_encode_word_to_ascii(self):
        """Testa conversão automática de símbolo textual/palavra para ASCII."""
        # 'O' = 79, 'i' = 105
        result = encode("Oi")
        assert result.numbers == [79, 105]

    def test_roundtrip_phrase(self):
        """Testa o ciclo completo com uma frase simples."""
        frase = "TP 2"
        resultado_enc = encode(frase)
        resultado_dec = decode(resultado_enc.encoded)
        
        # Converte a lista de inteiros de volta para texto
        texto_recuperado = "".join(chr(n) for n in resultado_dec.numbers)
        assert texto_recuperado == frase

class TestDecode:
    def test_returns_elias_gamma_decode_result(self):
        assert isinstance(decode("1"), EliasGammaDecodeResult)

    def test_simple_decode(self):
        assert decode("101000101").numbers == [1, 2, 5]

    def test_decode_result_fields(self):
        result = decode("1")
        assert result.binary == "1"
        assert result.total_bits == 1
        assert result.numbers == [1]

    def test_invalid_trailing_bits(self):
        with pytest.raises(ValueError):
            decode("001")

    def test_empty_binary_raises(self):
        with pytest.raises(ValueError):
            decode("")


class TestRoundtripNoError:
    @pytest.mark.parametrize("numbers", [
        [1],
        [1, 2, 3, 4, 5],
        [10, 20, 50, 100],
        [255, 256, 1024, 2048],
        [7, 14, 21, 28, 35],
    ])
    def test_roundtrip(self, numbers):
        result = encode(numbers)
        assert decode(result.encoded).numbers == numbers


class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        numbers = [10, 20, 30]
        result = encode(numbers)
        corrupted = flip_bit(result.encoded, 0)
        assert corrupted != result.encoded
        try:
            assert decode(corrupted).numbers != numbers
        except ValueError:
            pass

    def test_manual_error_indices(self):
        numbers = [5, 15, 25]
        result = encode(numbers)
        corrupted = result.encoded
        for idx in [1, 3]:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)
        assert corrupted != result.encoded
        try:
            assert decode(corrupted).numbers != numbers
        except ValueError:
            pass


class TestValidation:
    def test_encode_zero_raises(self):
        with pytest.raises(ValueError):
            encode([0])

    def test_encode_negative_raises(self):
        with pytest.raises(ValueError):
            encode([5, -2, 10])

    def test_encode_non_integer_raises(self):
        with pytest.raises(ValueError):
            encode([1, "dois", 3])
        with pytest.raises(ValueError):
            encode([1.5, 2])