"""
Command-line interface for encoding algorithms.
"""

import sys
from typing import Optional
from src.encoders import golomb, elias_gamma, fibonacci, huffman
from src.decoders import golomb_decoder, elias_gamma_decoder, fibonacci_decoder, huffman_decoder
from src.decoders.golomb_decoder import format_result as golomb_decode_fmt
from src.decoders.elias_gamma_decoder import format_result as elias_decode_fmt
from src.decoders.fibonacci_decoder import format_result as fib_decode_fmt
from src.decoders.huffman_decoder import format_result as huffman_decode_fmt
from src.utils.input_parser import (
    parse_integer_algorithm_input,
    format_ascii_mapping,
    format_input_metadata,
    format_reconstructed_decoding,
)

class EncoderCLI:
    """Command-line interface for encoding algorithms."""

    def __init__(self):
        """Initialize CLI."""
        self.algorithms = {
            '1': 'Golomb',
            '2': 'Elias-Gamma',
            '3': 'Fibonacci/Zeckendorf',
            '4': 'Huffman',
        }
        self.current_algo = None
        self.golomb_m = 4
        self.last_integer_metadata = {}

    def print_header(self):
        """Print application header."""
        print('\n' * 2)
        print("=" * 70)
        print(" " * 15 + "ALGORITMOS DE CODIFICAÇÃO")
        print("=" * 70)
        print()

    def print_menu(self):
        """Print main menu."""
        print("\n" + "─" * 70)
        print("MENU PRINCIPAL")
        print("─" * 70)
        print("1. Golomb")
        print("2. Elias-Gamma")
        print("3. Fibonacci/Zeckendorf")
        print("4. Huffman")
        print("5. Sair")
        print("─" * 70)

    def print_operation_menu(self):
        """Print operation menu."""
        print("\n" + "─" * 70)
        print("OPERAÇÃO")
        print("─" * 70)
        print("1. Codificar (Encode)")
        print("2. Decodificar (Decode)")
        print("3. Voltar ao menu principal")
        print("─" * 70)

    def get_input(self, prompt: str) -> Optional[str]:
        """Get user input."""
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\nOperação cancelada.")
            return None

    def select_algorithm(self) -> bool:
        """
        Let user select encoding algorithm.

        Returns:
            True if algorithm selected, False to exit
        """
        self.print_menu()
        choice = self.get_input("\nEscolha um algoritmo (1-5): ")

        if choice == '5':
            return False

        if choice not in self.algorithms:
            print("\nOpção inválida!")
            input("\nPressione Enter para continuar...")
            return True

        self.current_algo = self.algorithms[choice]

        if choice == '1':  # Golomb
            m_str = self.get_input("\nInforme o parâmetro m para Golomb (padrão=4): ")
            try:
                self.golomb_m = int(m_str) if m_str else 4
            except ValueError:
                print("\nValor inválido! Usando m=4")
                self.golomb_m = 4

        print(f"\n✓ Algoritmo selecionado: {self.current_algo}")
        return True

    def encode_operation(self):
        """Handle encoding operation. Returns (algo, codeword, metadata) or None."""
        print(f"\n{'─' * 70}")
        print(f"CODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        if self.current_algo == 'Huffman':
            text = self.get_input("\nInforme o texto a codificar: ")

            if not text:
                return None

            result = huffman.encode(text)
            print()
            print(huffman.format_result(result))
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
            result = golomb.encode(numbers, m=self.golomb_m)
            print(golomb.format_result(result))

        elif self.current_algo == 'Elias-Gamma':
            result = elias_gamma.encode(numbers)
            print(elias_gamma.format_result(result))

        elif self.current_algo == 'Fibonacci/Zeckendorf':
            result = fibonacci.encode(numbers)
            print(fibonacci.format_result(result))

        return (self.current_algo, result.encoded, {})

    def decode_operation(self):
        """Handle decoding operation."""
        print(f"\n{'─' * 70}")
        print(f"DECODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        binary = self.get_input("\nInforme o código binário: ")

        if not binary:
            return

        if self.current_algo == 'Huffman':
            print("\nPara Huffman, forneça a tabela de códigos.")
            print("Formato: char:code (separados por espaço)")
            print("Exemplo: a:0 b:10 c:11")

            codes_str = self.get_input("\nTabela de códigos: ")

            if not codes_str:
                return

            codes = {}

            for pair in codes_str.split():
                if ':' in pair:
                    char, code = pair.split(':', 1)
                    codes[char] = code

            binary_compact = "".join(binary.split())

            if not all(c in '01' for c in binary_compact):
                print("\n Código binário inválido! Use apenas 0 e 1.")
                return

            result = huffman_decoder.decode(binary_compact, codes)
            print()
            print(huffman_decode_fmt(result))
            return

        binary_compact = "".join(binary.split())

        if not all(c in '01' for c in binary_compact):
            print("\n Código binário inválido! Use apenas 0 e 1.")
            return

        if self.current_algo == 'Golomb':
            result = golomb_decoder.decode(binary_compact, m=self.golomb_m)
            print()
            print(golomb_decode_fmt(result))

        elif self.current_algo == 'Elias-Gamma':
            result = elias_gamma_decoder.decode(binary_compact)
            print()
            print(elias_decode_fmt(result))

        elif self.current_algo == 'Fibonacci/Zeckendorf':
            result = fibonacci_decoder.decode(binary_compact)
            print()
            print(fib_decode_fmt(result))

        metadata = self.last_integer_metadata.get(self.current_algo)
        print(format_reconstructed_decoding(result.numbers, metadata))

    def _maybe_send_to_server(self, algo: str, codeword: str, metadata: dict):
        """Ask the user whether to send the codeword to the error-correction server."""
        answer = self.get_input("\nEnviar ao servidor para verificação de erros? (s/n): ")
        if not answer or answer.lower() != 's':
            return

        from src.network.client import send_codeword  # lazy import — no server needed at startup

        print("\nConectando ao servidor (127.0.0.1:9000)...")
        try:
            resp = send_codeword(algo, codeword, metadata)
        except TimeoutError as exc:
            print(f"\n Sem resposta: {exc}")
            return
        except OSError as exc:
            print(f"\n Erro de rede: {exc}")
            return

        print("\n" + "─" * 70)
        print("RESPOSTA DO SERVIDOR")
        print("─" * 70)
        print(f"Recebido  : {codeword[:60]}{'...' if len(codeword) > 60 else ''}")
        print(f"Corrigido : {resp['corrected_codeword'][:60]}{'...' if len(resp['corrected_codeword']) > 60 else ''}")
        erro_str = f"Posição {resp['error_position']}" if resp['error_detected'] else "Não detectado"
        print(f"Erro      : {erro_str}")
        print(f"Mensagem  : {resp['message']}")
        print("─" * 70)

    def run_operations(self):
        """Run encoding/decoding operations loop."""
        while True:
            self.print_operation_menu()
            choice = self.get_input("\nEscolha uma operação (1-3): ")

            if choice == '3':
                break
            elif choice == '1':
                encoded = self.encode_operation()
                if encoded:
                    self._maybe_send_to_server(*encoded)
            elif choice == '2':
                self.decode_operation()
            else:
                print("\n Opção inválida!")

            input("\nPressione Enter para continuar...")

    def run(self):
        """Run the CLI application."""
        try:
            while True:
                self.print_header()

                if not self.select_algorithm():
                    break

                self.run_operations()
                self.current_algo = None

            print("\n Até logo!\n")

        except KeyboardInterrupt:
            print("\n\n Programa encerrado pelo usuário.\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n Erro inesperado: {e}\n")
            sys.exit(1)


def main():
    """Main entry point."""
    cli = EncoderCLI()
    cli.run()


if __name__ == '__main__':
    main()