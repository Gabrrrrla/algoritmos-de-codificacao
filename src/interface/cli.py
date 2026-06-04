"""
Command-line interface for encoding algorithms.
"""

import sys
from typing import Optional
from src.algorithms import (
    golomb as alg_golomb,
    elias_gamma as alg_elias,
    fibonacci as alg_fibonacci,
    huffman as alg_huffman,
    repetition as alg_repetition,
    hamming as alg_hamming,
    crc as alg_crc,
)
from src.utils.huffman_input_parser import parse_huffman_decode_input
from src.utils.input_parser import (
    parse_integer_algorithm_input,
    format_ascii_mapping,
    format_input_metadata,
    format_reconstructed_decoding,
)
from src.network.client import check_server, send_codeword

_ERROR_ALGOS = {"Repetição Ri", "Hamming (7,4)", "CRC-4"}


class EncoderCLI:
    """Command-line interface for encoding algorithms."""

    def __init__(self):
        self.algorithms = {
            '1': 'Golomb',
            '2': 'Elias-Gamma',
            '3': 'Fibonacci/Zeckendorf',
            '4': 'Huffman',
            '5': 'Repetição Ri',
            '6': 'Hamming (7,4)',
            '7': 'CRC-4',
        }
        self.current_algo = None
        self.golomb_m = 4
        self.repetition_r = 3
        self.last_integer_metadata = {}

    def print_header(self):
        print('\n' * 2)
        print("=" * 70)
        print(" " * 15 + "ALGORITMOS DE CODIFICAÇÃO")
        print("=" * 70)
        print()

    def print_menu(self):
        print("\n" + "─" * 70)
        print("MENU PRINCIPAL")
        print("─" * 70)
        print("1. Golomb")
        print("2. Elias-Gamma")
        print("3. Fibonacci/Zeckendorf")
        print("4. Huffman")
        print("5. Repetição Ri")
        print("6. Hamming (7,4)")
        print("7. CRC-4")
        print("8. Sair")
        print("─" * 70)

    def print_operation_menu(self):
        print("\n" + "─" * 70)
        print("OPERAÇÃO")
        print("─" * 70)
        print("1. Codificar (Encode)")
        print("2. Decodificar (Decode)")
        print("3. Voltar ao menu principal")
        print("─" * 70)

    def get_input(self, prompt: str) -> Optional[str]:
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\nOperação cancelada.")
            return None

    def select_algorithm(self) -> bool:
        self.print_menu()
        choice = self.get_input("\nEscolha um algoritmo (1-8): ")

        if choice == '8':
            return False

        if choice not in self.algorithms:
            print("\nOpção inválida!")
            input("\nPressione Enter para continuar...")
            return True

        self.current_algo = self.algorithms[choice]

        if choice == '1':
            m_str = self.get_input("\nInforme o parâmetro m para Golomb (padrão=4): ")
            try:
                self.golomb_m = int(m_str) if m_str else 4
            except ValueError:
                print("\nValor inválido! Usando m=4")
                self.golomb_m = 4

        if choice == '5':
            r_str = self.get_input("\nInforme o fator de repetição r (padrão=3, deve ser ímpar): ")
            try:
                self.repetition_r = int(r_str) if r_str else 3
                if self.repetition_r < 1:
                    raise ValueError
            except ValueError:
                print("\nValor inválido! Usando r=3")
                self.repetition_r = 3

        print(f"\n✓ Algoritmo selecionado: {self.current_algo}")
        return True

    # ─────────────────────── encode ──────────────────────────────────

    def encode_operation(self):
        """Handle encoding for compression algorithms. Returns (algo, codeword, metadata) or None."""
        print(f"\n{'─' * 70}")
        print(f"CODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        if self.current_algo == 'Huffman':
            text = self.get_input("\nInforme o texto a codificar: ")
            if not text:
                return None
            result = alg_huffman.encode(text)
            print()
            print(alg_huffman.format_result(result))
            return (self.current_algo, result.encoded, {"code_table": result.code_table})

        input_str = self.get_input(
            "\nInforme números, texto, palavras ou símbolos separados por espaço/vírgula: "
        )
        if not input_str:
            return None

        try:
            parsed = parse_integer_algorithm_input(input_str, positive_only=True)
        except (TypeError, ValueError) as exc:
            print(f"\nEntrada inválida! {exc}")
            return None

        numbers = parsed.numbers
        self.last_integer_metadata[self.current_algo] = parsed.metadata

        print()
        print(f"Tokens de entrada : {parsed.tokens}")
        print(format_input_metadata(parsed.metadata))

        if parsed.ascii_mapping:
            print(format_ascii_mapping(parsed.ascii_mapping))

        if self.current_algo == 'Golomb':
            result = alg_golomb.encode(numbers, m=self.golomb_m)
            print(alg_golomb.format_result(result))

        elif self.current_algo == 'Elias-Gamma':
            result = alg_elias.encode(numbers)
            print(alg_elias.format_result(result))

        elif self.current_algo == 'Fibonacci/Zeckendorf':
            result = alg_fibonacci.encode(numbers)
            print(alg_fibonacci.format_result(result))

        return (self.current_algo, result.encoded, {})

    def _encode_error_correction(self):
        """Handle encode for Repetição Ri, Hamming (7,4) and CRC-4. Returns (algo, codeword, metadata) or None."""
        print(f"\n{'─' * 70}")
        print(f"CODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        binary = self.get_input("\nInforme a string binária a codificar: ")
        if not binary:
            return None

        binary_clean = binary.replace(" ", "")
        if not all(b in "01" for b in binary_clean):
            print("\nEntrada inválida! Use apenas 0 e 1.")
            return None

        if self.current_algo == 'Repetição Ri':
            result = alg_repetition.encode(binary_clean, r=self.repetition_r)
            print()
            print(alg_repetition.format_encode_result(result))
            return (self.current_algo, result.encoded, {"r": self.repetition_r})

        if self.current_algo == 'Hamming (7,4)':
            result = alg_hamming.encode(binary_clean)
            print()
            print(alg_hamming.format_encode_result(result))
            return (self.current_algo, result.encoded, {})

        if self.current_algo == 'CRC-4':
            result = alg_crc.encode(binary_clean)
            print()
            print(alg_crc.format_encode_result(result))
            return (self.current_algo, result.transmitted, {})

        return None

    # ─────────────────────── decode ──────────────────────────────────

    def _decode_error_correction(self):
        """Handle decode/check for Repetição Ri, Hamming (7,4) and CRC-4."""
        print(f"\n{'─' * 70}")
        print(f"DECODIFICAÇÃO / VERIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        binary = self.get_input("\nInforme o código binário recebido: ")
        if not binary:
            return

        binary_clean = binary.replace(" ", "")
        if not all(b in "01" for b in binary_clean):
            print("\nEntrada inválida! Use apenas 0 e 1.")
            return

        if self.current_algo == 'Repetição Ri':
            result = alg_repetition.decode(binary_clean, r=self.repetition_r)
            print()
            print(alg_repetition.format_decode_result(result))

        elif self.current_algo == 'Hamming (7,4)':
            result = alg_hamming.decode(binary_clean)
            print()
            print(alg_hamming.format_decode_result(result))

        elif self.current_algo == 'CRC-4':
            result = alg_crc.check(binary_clean)
            print()
            print(alg_crc.format_check_result(result))

    def decode_operation(self):
        """Handle decoding for compression algorithms."""
        print(f"\n{'─' * 70}")
        print(f"DECODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        if self.current_algo == 'Huffman':
            raw = self.get_input(
                "\nInforme o código binário e a tabela Huffman.\n"
                "Exemplo: 1001011110100110 !:00, a:01, Á:100, g:101, @:110, u:111\n> "
            )
            if not raw:
                return
            binary, codes = parse_huffman_decode_input(raw)
            result = alg_huffman.decode(binary, codes)
            print()
            print(alg_huffman.format_decode_result(result))
            return

        binary = self.get_input("\nInforme o código binário: ")
        if not binary:
            return

        binary_compact = "".join(binary.split())
        if not all(c in '01' for c in binary_compact):
            print("\nCódigo binário inválido! Use apenas 0 e 1.")
            return

        if self.current_algo == 'Golomb':
            result = alg_golomb.decode(binary_compact, m=self.golomb_m)
            print()
            print(alg_golomb.format_decode_result(result))

        elif self.current_algo == 'Elias-Gamma':
            result = alg_elias.decode(binary_compact)
            print()
            print(alg_elias.format_decode_result(result))

        elif self.current_algo == 'Fibonacci/Zeckendorf':
            result = alg_fibonacci.decode(binary_compact)
            print()
            print(alg_fibonacci.format_decode_result(result))

        metadata = self.last_integer_metadata.get(self.current_algo)
        print(format_reconstructed_decoding(result.numbers, metadata))

    # ─────────────────────── server ──────────────────────────────────

    def _ask_error_injection(self, codeword: str) -> list[int]:
        """Ask for bit indices to flip. Returns the list of indices (may be empty)."""
        raw = self.get_input(
            "\nInjetar erros? Informe índices dos bits a inverter separados por vírgula\n"
            "(deixe vazio para nenhum): "
        )
        if not raw:
            return []

        try:
            indices = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print("\nÍndices inválidos — nenhum erro injetado.")
            return []

        if any(idx < 0 for idx in indices):
            print("\nÍndices devem ser ≥ 0 — nenhum erro injetado.")
            return []

        return indices

    @staticmethod
    def _inject_errors(codeword: str, indices: list[int]) -> str:
        char_list = list(codeword)
        bit_idx = 0
        for i, char in enumerate(char_list):
            if char in "01":
                if bit_idx in indices:
                    char_list[i] = "1" if char == "0" else "0"
                bit_idx += 1
        return "".join(char_list)

    def _send_to_server(self, algo: str, clean_codeword: str, metadata: dict, error_indices: list[int]):
        """Check server and send automatically. Wraps compression codewords with CRC first,
        then injects errors on the full frame so the server can detect them."""
        if not check_server():
            print("\n⚠  Servidor offline — resultado calculado localmente.")
            return

        if algo not in _ERROR_ALGOS:
            crc_result = alg_crc.encode(clean_codeword)
            frame = crc_result.transmitted
            send_algo = "CRC-4"
            send_metadata = {}
        else:
            frame = clean_codeword
            send_algo = algo
            send_metadata = metadata

        if error_indices:
            corrupted = self._inject_errors(frame, error_indices)
            print(f"\nFrame original    : {frame}")
            print(f"Frame com erro    : {corrupted}")
            frame = corrupted

        print("\nEnviando ao servidor (127.0.0.1:9000)...")
        try:
            resp = send_codeword(send_algo, frame, send_metadata)
        except TimeoutError as exc:
            print(f"\n⚠  Sem resposta do servidor: {exc}")
            return
        except OSError as exc:
            print(f"\n❌  Erro de rede: {exc}")
            return
        except Exception as exc:
            print(f"\n❌  Erro inesperado: {exc}")
            return

        pos = resp["error_position"]
        if not resp["error_detected"]:
            erro_str = "Não detectado"
        elif pos is not None:
            erro_str = f"Posição {pos}"
        else:
            erro_str = "Detectado (posição não localizável pelo algoritmo)"

        print("\n" + "─" * 70)
        print("RESPOSTA DO SERVIDOR (127.0.0.1:9000)")
        print("─" * 70)
        print(f"Enviado   : {frame}")
        print(f"Corrigido : {resp['corrected_codeword']}")
        print(f"Erro      : {erro_str}")
        print(f"Mensagem  : {resp['message']}")
        print("─" * 70)

    # ─────────────────────── main loop ───────────────────────────────

    def run_operations(self):
        is_error_algo = self.current_algo in _ERROR_ALGOS
        while True:
            self.print_operation_menu()
            choice = self.get_input("\nEscolha uma operação (1-3): ")

            if choice == '3':
                break
            elif choice == '1':
                encoded = self._encode_error_correction() if is_error_algo else self.encode_operation()
                if encoded:
                    algo, clean_codeword, metadata = encoded
                    error_indices = self._ask_error_injection(clean_codeword)
                    self._send_to_server(algo, clean_codeword, metadata, error_indices)
            elif choice == '2':
                if is_error_algo:
                    self._decode_error_correction()
                else:
                    self.decode_operation()
            else:
                print("\nOpção inválida!")

            input("\nPressione Enter para continuar...")

    def run(self):
        try:
            while True:
                self.print_header()

                if not self.select_algorithm():
                    break

                self.run_operations()
                self.current_algo = None

            print("\nAté logo!\n")

        except KeyboardInterrupt:
            print("\n\nPrograma encerrado pelo usuário.\n")
            sys.exit(0)
        except Exception as e:
            print(f"\nErro inesperado: {e}\n")
            sys.exit(1)


def main():
    cli = EncoderCLI()
    cli.run()


if __name__ == '__main__':
    main()
