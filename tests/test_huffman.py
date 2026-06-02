"""
Testes integrados para o módulo Huffman.

Cobre:
  - Entrada textual e construção de árvore/tabela
  - Codificação e decodificação (roundtrip)
  - Empacotamento e desempacotamento para Socket
  - Inserção manual de erro em bits
  - Verificação de falha na decodificação com erro
  - Casos-limite (1 caractere, texto longo, caracteres especiais)
"""

import pytest
import json
from src.algorithms.huffman import (
    build_frequency_table,
    build_tree,
    build_code_table,
    encode,
    format_for_socket,
    HuffmanNode,
    HuffmanResult,
)
from src.algorithms.huffman import (
    decode,
    parse_from_socket,
    HuffmanDecodeResult
)


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição `index`."""
    bits = list(binary)
    if bits[index] == "0":
        bits[index] = "1"
    else:
        bits[index] = "0"
    return "".join(bits)


# ── Tabela de frequências ─────────────────────────────────────────────

class TestFrequencyTable:
    def test_simple(self):
        assert build_frequency_table("aab") == {"a": 2, "b": 1}

    def test_single_char(self):
        assert build_frequency_table("aaaa") == {"a": 4}

    def test_all_unique(self):
        freq = build_frequency_table("abcd")
        assert all(v == 1 for v in freq.values())
        assert len(freq) == 4


# ── Construção da árvore ──────────────────────────────────────────────

class TestBuildTree:
    def test_returns_node(self):
        root = build_tree({"a": 3, "b": 1})
        assert isinstance(root, HuffmanNode)

    def test_root_freq_is_total(self):
        freq = {"a": 5, "b": 3, "c": 2}
        root = build_tree(freq)
        assert root.freq == 10

    def test_single_symbol(self):
        root = build_tree({"x": 7})
        # Deve ter pelo menos um filho.
        assert root.left is not None or root.right is not None


# ── Tabela de códigos ─────────────────────────────────────────────────

class TestCodeTable:
    def test_all_chars_present(self):
        freq = {"a": 5, "b": 3, "c": 2}
        tree = build_tree(freq)
        codes = build_code_table(tree)
        assert set(codes.keys()) == {"a", "b", "c"}

    def test_codes_are_binary_strings(self):
        tree = build_tree({"a": 1, "b": 1, "c": 1})
        codes = build_code_table(tree)
        for code in codes.values():
            assert all(bit in "01" for bit in code)

    def test_prefix_free(self):
        tree = build_tree({"a": 5, "b": 3, "c": 1, "d": 1})
        codes = build_code_table(tree)
        code_list = sorted(codes.values())
        for i in range(len(code_list) - 1):
            assert not code_list[i + 1].startswith(code_list[i])

    def test_single_symbol_gets_code(self):
        tree = build_tree({"z": 10})
        codes = build_code_table(tree)
        assert codes == {"z": "0"}


# ── Encode ────────────────────────────────────────────────────────────

class TestEncode:
    def test_returns_huffman_result(self):
        result = encode("abc")
        assert isinstance(result, HuffmanResult)

    def test_encoded_is_binary_string(self):
        result = encode("hello world")
        assert all(bit in "01" for bit in result.encoded)

    def test_length_matches(self):
        text = "abracadabra"
        result = encode(text)
        expected_len = sum(len(result.code_table[ch]) for ch in text)
        assert len(result.encoded) == expected_len

    def test_rate_is_positive(self):
        result = encode("abracadabra")
        assert result.rate > 0

    def test_total_bits_matches_encoded(self):
        result = encode("abracadabra")
        assert result.total_bits == len(result.encoded)


# ── Empacotamento para Socket ───────────────────────────────────

class TestSocketPackaging:
    def test_format_for_socket(self):
        result = encode("OI")
        payload = format_for_socket(result)
        
        assert "|" in payload
        table_json, binary = payload.split("|", 1)
        
        assert json.loads(table_json) == result.code_table
        assert binary == result.encoded

    def test_parse_from_socket(self):
        payload = '{"A": "0", "B": "10", "C": "11"}|01011'
        code_table, binary = parse_from_socket(payload)
        
        assert code_table == {"A": "0", "B": "10", "C": "11"}
        assert binary == "01011"

    def test_parse_invalid_payload_raises(self):
        with pytest.raises(ValueError, match="Payload inválido"):
            parse_from_socket("STRING_SEM_BARRA_VERTICAL")


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_returns_huffman_decode_result(self):
        codes = {"a": "0", "b": "10", "c": "11"}
        assert isinstance(decode("01011", codes), HuffmanDecodeResult)

    def test_simple_decode(self):
        codes = {"a": "0", "b": "10", "c": "11"}
        assert decode("01011", codes).text == "abc"

    def test_decode_result_fields(self):
        codes = {"a": "0", "b": "10", "c": "11"}
        result = decode("01011", codes)
        assert result.binary == "01011"
        assert result.total_bits == 5
        assert result.codes == codes

    def test_invalid_trailing_bits(self):
        codes = {"a": "0", "b": "10"}
        with pytest.raises(ValueError, match="sobrou"):
            decode("01", codes)  # "01" → 'a' + sobra '1'

    def test_empty_binary_raises(self):
        with pytest.raises(ValueError):
            decode("", {"a": "0"})

    def test_empty_codes_raises(self):
        with pytest.raises(ValueError):
            decode("010", {})


# ── Roundtrip (encode → decode) SEM erro ──────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("text", [
        "brizola",
        "hello world",
        "aaaaaaa",
        "abcdefghijklmnopqrstuvwxyz",
        "Bobajadaaa!",
        "🎉🎉🎉",
        "a",
        "10 20 30",  # Teste de strings numéricas exigidas
    ])
    def test_roundtrip(self, text):
        # Usando o fluxo de Sockets completo
        enc_result = encode(text)
        payload = format_for_socket(enc_result)
        
        tabela_recebida, bits_recebidos = parse_from_socket(payload)
        decoded = decode(bits_recebidos, tabela_recebida)
        
        assert decoded.text == text


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        text = "abracadabra"
        result = encode(text)

        corrupted = flip_bit(result.encoded, 0)
        assert corrupted != result.encoded

        # A decodificação pode:
        #   (a) retornar texto diferente do original, ou
        #   (b) lançar ValueError se a sequência corrompida for inválida.
        try:
            decoded = decode(corrupted, result.code_table)
            assert decoded.text != text, (
                "Esperava-se que o texto decodificado fosse diferente após flip de bit.")
        except ValueError:
            pass

    def test_multiple_bit_flips(self):
        text = "hello world"
        result = encode(text)

        corrupted = result.encoded
        for idx in [0, 2, 4]:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)

        try:
            decoded = decode(corrupted, result.code_table)
            assert decoded.text != text
        except ValueError:
            pass

    def test_manual_error_indices(self):
        """Simula o mecanismo de inserção manual de erro por índices."""
        text = "teste de erro"
        result = encode(text)

        error_indices = [1, 3]
        corrupted = result.encoded
        for idx in error_indices:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)

        assert corrupted != result.encoded

        try:
            decoded = decode(corrupted, result.code_table)
            assert decoded.text != text
        except ValueError:
            pass


# ── Validações de entrada ──────────────────────────────────────────────

class TestValidation:
    def test_encode_empty_raises(self):
        with pytest.raises(ValueError):
            encode("")

    def test_encode_non_string_raises(self):
        with pytest.raises(TypeError):
            encode(123)

    def test_decode_non_binary_raises(self):
        with pytest.raises(ValueError):
            decode("abc", {"a": "0"})

    def test_decode_prefix_conflict_raises(self):
        with pytest.raises(ValueError, match="prefixo"):
            decode("010", {"a": "0", "b": "01"})