"""
Testes integrados para o módulo Golomb.

Cobre:
  - Codificação de valores individuais e listas
  - Decodificação
  - Roundtrip (encode → decode) sem erro
  - Roundtrip com inserção de erro em bits
  - Diferentes valores de m (1, 2, 4, 8, potência de 2 e não-potência)
  - Validações de entrada
"""

import pytest
from src.algorithms.golomb import encode, GolombResult
from src.algorithms.golomb import decode, GolombDecodeResult


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição `index` (ignora espaços na contagem)."""
    bits = list(binary)
    bit_idx = 0
    for i, char in enumerate(bits):
        if char in "01":
            if bit_idx == index:
                bits[i] = "1" if char == "0" else "0"
                return "".join(bits)
            bit_idx += 1
    raise IndexError(f"Índice de bit {index} fora do alcance.")


# ── Encode: valores individuais ───────────────────────────────────────

class TestEncodeSingle:
    def test_encode_1_m4(self):
        assert encode(1, m=4).encoded == "001"

    def test_returns_golomb_result(self):
        result = encode(5, m=4)
        assert isinstance(result, GolombResult)

    def test_encoded_is_binary_string(self):
        result = encode(5, m=4)
        assert isinstance(result.encoded, str)
        assert all(c in "01 " for c in result.encoded)

    def test_encode_m1(self):
        assert encode(1, m=1).encoded == "10"
        assert encode(3, m=1).encoded == "1110"

    def test_encode_m2(self):
        assert encode(1, m=2).encoded == "01"
        assert encode(2, m=2).encoded == "10"

    def test_result_fields(self):
        result = encode(5, m=4)
        assert result.m == 4
        assert result.numbers == [5]
        assert result.total_bits == len(result.encoded)
        assert result.rate > 0


# ── Encode: listas e textos  ─────────────────────────────────────

class TestEncodeListAndText:
    def test_encode_list(self):
        result = encode([1, 2, 3], m=4)
        # Como alteramos para bitstream contínuo, pode não ter espaços
        assert result.encoded == "001010011" or result.encoded == "001 010 011"

    def test_encode_list_m1(self):
        result = encode([1, 2, 3], m=1)
        assert "10" in result.encoded
        assert "110" in result.encoded
        assert "1110" in result.encoded

    def test_encode_string_of_numbers(self):
        """Testa entrada múltipla separada por espaço."""
        result = encode("10 20 30", m=4)
        assert result.numbers == [10, 20, 30]

    def test_encode_string_of_numbers_with_comma(self):
        """Testa entrada múltipla separada por vírgula."""
        result = encode("10, 20, 30", m=4)
        assert result.numbers == [10, 20, 30]

    def test_encode_word_to_ascii(self):
        """Testa conversão automática de símbolo textual/palavra para ASCII."""
        # 'O' = 79, 'i' = 105
        result = encode("Oi", m=4)
        assert result.numbers == [79, 105]

    def test_roundtrip_phrase(self):
        """Testa o ciclo completo com uma frase simples."""
        frase = "Golomb"
        resultado_enc = encode(frase, m=4)
        resultado_dec = decode(resultado_enc.encoded, m=4)
        
        texto_recuperado = "".join(chr(n) for n in resultado_dec.numbers)
        assert texto_recuperado == frase


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_returns_golomb_decode_result(self):
        result = decode("000", m=4)
        assert isinstance(result, GolombDecodeResult)

    def test_decode_single(self):
        assert decode("000", m=4).numbers == [0]

    def test_decode_m1(self):
        assert decode("0", m=1).numbers == [0]
        assert decode("110", m=1).numbers == [2]

    def test_decode_m2(self):
        assert decode("00", m=2).numbers == [0]
        assert decode("01", m=2).numbers == [1]

    def test_decode_result_fields(self):
        result = decode("000", m=4)
        assert result.m == 4
        assert result.total_bits == 3
        assert result.binary == "000"

    def test_decode_multiple_concatenated(self):
        encoded = encode([1, 2, 3], m=4).encoded.replace(" ", "")
        assert decode(encoded, m=4).numbers == [1, 2, 3]


# ── Roundtrip SEM erro ────────────────────────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("m", [1, 2, 3, 4, 5, 7, 8, 16])
    def test_roundtrip_single(self, m):
        for n in [0, 1, 2, 3, 5, 10, 20]:
            encoded = encode(n, m=m).encoded.replace(" ", "")
            decoded = decode(encoded, m=m).numbers
            assert decoded == [n], f"Falha: n={n}, m={m}"

    @pytest.mark.parametrize("m", [1, 2, 4, 8])
    def test_roundtrip_list(self, m):
        numbers = [1, 3, 5, 7, 10, 15]
        encoded = encode(numbers, m=m).encoded.replace(" ", "")
        assert decode(encoded, m=m).numbers == numbers

    def test_roundtrip_large_values(self):
        numbers = [50, 100, 200]
        for m in [4, 7, 16]:
            encoded = encode(numbers, m=m).encoded.replace(" ", "")
            assert decode(encoded, m=m).numbers == numbers


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip(self):
        numbers = [1, 3, 5, 7]
        encoded = encode(numbers, m=4).encoded.replace(" ", "")
        corrupted = flip_bit(encoded, 0)
        assert corrupted != encoded
        try:
            assert decode(corrupted, m=4).numbers != numbers
        except ValueError:
            pass

    def test_multiple_bit_flips(self):
        numbers = [2, 4, 6, 8]
        encoded = encode(numbers, m=4).encoded.replace(" ", "")
        corrupted = encoded
        for idx in [0, 2, 4]:
            if idx < len(corrupted.replace(" ", "")):
                corrupted = flip_bit(corrupted, idx)
        try:
            assert decode(corrupted, m=4).numbers != numbers
        except ValueError:
            pass


# ── Valores de m não-potência de 2 ────────────────────────────────────

class TestNonPowerOfTwo:
    @pytest.mark.parametrize("m", [3, 5, 6, 7, 9, 10])
    def test_roundtrip_non_power_of_two(self, m):
        numbers = [1, 2, 4, 8, 12]
        encoded = encode(numbers, m=m).encoded.replace(" ", "")
        assert decode(encoded, m=m).numbers == numbers


# ── Validações de entrada ──────────────────────────────────────────────

class TestValidation:
    def test_encode_zero(self):
        result = encode(0, m=4)
        assert result.encoded == "000"

    def test_encode_negative_raises(self):
        with pytest.raises(ValueError):
            encode(-1, m=4)

    def test_encode_m_zero_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=0)

    def test_encode_m_negative_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=-1)

    def test_encode_m_bool_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=True)

    def test_decode_empty_raises(self):
        with pytest.raises(ValueError):
            decode("", m=4)

    def test_decode_invalid_binary_raises(self):
        with pytest.raises(ValueError):
            decode("abc", m=4)

    def test_decode_incomplete_raises(self):
        with pytest.raises(ValueError):
            decode("1", m=4)