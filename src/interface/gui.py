"""
Graphical User Interface for encoding algorithms using customtkinter.

Layout:
  - Left sidebar : 4 algorithm buttons + appearance / scaling controls
  - Center panel : row 0 → title + Golomb-m (same row, title left / m right)
                   row 1 → encode/decode radio buttons
                   row 2 → "Entrada" label
                   row 3 → input textbox  (expands)
                   row 4 → submit button (col 0) + error injection (col 1)
                   row 5 → "Resultado" label
                   row 6 → output textbox (expands)
                   row 7 → error label
"""

import sys
import tkinter as tk
from io import StringIO
from typing import Optional
from src.utils.huffman_input_parser import parse_huffman_decode_input
from src.utils.input_parser import (
    parse_integer_algorithm_input,
    format_ascii_mapping,
    format_input_metadata,
    format_reconstructed_decoding,
)

import customtkinter
from src.algorithms import golomb as golomb_encoder, elias_gamma as elias_gamma_encoder, fibonacci as fibonacci_encoder, huffman as huffman_encoder, repetition as repetition_encoder, hamming as hamming_encoder, crc as crc_encoder
from src.algorithms import golomb as golomb_decoder, elias_gamma as elias_gamma_decoder, fibonacci as fibonacci_decoder, huffman as huffman_decoder

# ── default appearance ────────────────────────────────────────────────
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class EncoderApp(customtkinter.CTk):
    """Main application window."""

    ALGORITHMS = ["Golomb", "Elias-Gamma", "Fibonacci/Zeckendorf", "Huffman", "Repetição Ri", "Hamming (7,4)", "CRC-4"]

    def __init__(self):
        super().__init__()

        self.title("Algoritmos de Codificação")
        self.geometry("960x620")
        self.minsize(820, 520)

        # ── state variables ──────────────────────────────────────────
        self.selected_algo       = tk.StringVar(value=self.ALGORITHMS[0])
        self.operation           = tk.StringVar(value="encode")
        self.golomb_m            = tk.StringVar(value="4")
        self.repetition_r        = tk.StringVar(value="3")
        self._placeholder_active = False
        self._HUFFMAN_PLACEHOLDER = "1001011110100110 !:00, a:01, Á:100, g:101, @:110, u:111"
        self._last_server_payload: Optional[tuple] = None  # (algo, clean_codeword, metadata, error_indices)

        # grid: sidebar (col 0) | center (col 1, expands)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_center()
        self._last_integer_metadata = {}

        # highlight first algorithm button
        self._select_algo(self.ALGORITHMS[0])

    # ─────────────────────────── sidebar ─────────────────────────────

    def _build_sidebar(self):
        sb = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        n = len(self.ALGORITHMS)
        sb.grid_rowconfigure(n + 1, weight=1)  # spacer — pushes appearance controls to bottom

        customtkinter.CTkLabel(
            sb,
            text="Algoritmos",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(24, 14), sticky="w")

        self._algo_buttons: dict[str, customtkinter.CTkButton] = {}
        for i, name in enumerate(self.ALGORITHMS):
            btn = customtkinter.CTkButton(
                sb,
                text=name,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray30"),
                command=lambda n=name: self._select_algo(n),
            )
            btn.grid(row=i + 1, column=0, padx=12, pady=4, sticky="ew")
            self._algo_buttons[name] = btn

        # appearance / scaling at bottom
        customtkinter.CTkLabel(sb, text="Aparência:", anchor="w").grid(
            row=n + 2, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self._appearance_menu = customtkinter.CTkOptionMenu(
            sb,
            values=["Dark", "Light", "System"],
            command=lambda v: customtkinter.set_appearance_mode(v),
        )
        self._appearance_menu.set("Dark")
        self._appearance_menu.grid(row=n + 3, column=0, padx=20, pady=(4, 8), sticky="ew")

        customtkinter.CTkLabel(sb, text="Escala:", anchor="w").grid(
            row=n + 4, column=0, padx=20, pady=(4, 0), sticky="w"
        )
        self._scaling_menu = customtkinter.CTkOptionMenu(
            sb,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self._change_scaling,
        )
        self._scaling_menu.set("100%")
        self._scaling_menu.grid(row=n + 5, column=0, padx=20, pady=(4, 20), sticky="ew")

    # ─────────────────────────── center ──────────────────────────────

    def _build_center(self):
        center = customtkinter.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew", padx=30, pady=28)

        # col 0 expands; col 1 is fixed (Golomb m / error injection widgets)
        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=0)
        # input and output rows expand vertically
        center.grid_rowconfigure(3, weight=2)
        center.grid_rowconfigure(6, weight=3)

        # ── row 0: title (col 0) + Golomb m (col 1) ──────────────────
        self._title_label = customtkinter.CTkLabel(
            center, text="", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self._title_label.grid(row=0, column=0, sticky="w", pady=(0, 12))

        self._golomb_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        self._golomb_frame.grid(row=0, column=1, sticky="ew", padx=(20, 0), pady=(0, 12))
        customtkinter.CTkLabel(
            self._golomb_frame, text="m :", anchor="e", width=118
        ).pack(side="left", padx=(0, 6))
        customtkinter.CTkEntry(
            self._golomb_frame,
            textvariable=self.golomb_m,
            width=150,
            placeholder_text="4",
        ).pack(side="left")
        self._golomb_frame.grid_remove()   # hidden until Golomb is selected

        self._repetition_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        self._repetition_frame.grid(row=0, column=1, sticky="ew", padx=(20, 0), pady=(0, 12))
        customtkinter.CTkLabel(
            self._repetition_frame, text="r :", anchor="e", width=118
        ).pack(side="left", padx=(0, 6))
        customtkinter.CTkEntry(
            self._repetition_frame,
            textvariable=self.repetition_r,
            width=150,
            placeholder_text="3",
        ).pack(side="left")
        self._repetition_frame.grid_remove()   # hidden until Repetição Ri is selected

        # ── row 1: encode / decode radio buttons ──────────────────────
        radio_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        radio_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 12))
        self._radio_encode = customtkinter.CTkRadioButton(
            radio_frame,
            text="Codificar",
            variable=self.operation,
            value="encode",
            command=self._on_operation_change,
        )
        self._radio_encode.pack(side="left", padx=(0, 24))
        self._radio_decode = customtkinter.CTkRadioButton(
            radio_frame,
            text="Decodificar",
            variable=self.operation,
            value="decode",
            command=self._on_operation_change,
        )
        self._radio_decode.pack(side="left")

        # ── row 2: input label ─────────────────────────────────────────
        customtkinter.CTkLabel(center, text="Entrada", anchor="w").grid(
            row=2, column=0, columnspan=2, sticky="w"
        )

        # ── row 3: input textbox ───────────────────────────────────────
        self._input_box = customtkinter.CTkTextbox(
            center,
            font=customtkinter.CTkFont(family="Courier", size=14),
            border_spacing=14,
        )
        self._input_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        # Bind focus events for placeholder simulation
        self._input_box._textbox.bind("<FocusIn>", self._on_input_focus_in, add="+")
        self._input_box._textbox.bind("<FocusOut>", self._on_input_focus_out, add="+")
        self._input_box._textbox.bind("<Button-1>", self._on_input_focus_in, add="+")
        self._input_box._textbox.bind("<KeyPress>", self._on_input_key_press, add="+")

        # ── row 4: submit button (col 0) + error injection (col 1) ────

        # ── submit + send-to-server buttons ───────────────────────
        btn_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        btn_frame.grid(row=4, column=0, pady=14, sticky="w")

        customtkinter.CTkButton(
            btn_frame,
            text="▶   Executar",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            command=self._submit,
        ).pack(side="left", padx=(0, 12))

        self._send_btn = customtkinter.CTkButton(
            btn_frame,
            text="⇪   Enviar ao Servidor",
            font=customtkinter.CTkFont(size=13),
            state="disabled",
            command=self._send_to_server,
        )
        self._send_btn.pack(side="left")

        self._server_status_label = customtkinter.CTkLabel(
            btn_frame,
            text="● Servidor: —",
            font=customtkinter.CTkFont(size=12),
            text_color="gray50",
        )
        self._server_status_label.pack(side="left", padx=(16, 0))

        # ── error injection ─────────────────────────────────────────

        self._error_injection_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        self._error_injection_frame.grid(row=4, column=1, sticky="ew", padx=(20, 0), pady=14)

        customtkinter.CTkLabel(
            self._error_injection_frame, text="Force Error:", anchor="e", width=118
        ).pack(side="left", padx=(0, 6))

        self._error_entry = customtkinter.CTkEntry(
            self._error_injection_frame,
            width=150,
            placeholder_text="Ex: 0, 3, 5",
        )
        self._error_entry.pack(side="left")

        # ── row 5: output label ────────────────────────────────────────
        customtkinter.CTkLabel(center, text="Resultado", anchor="w").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )

        # ── row 6: output textbox (read-only) ─────────────────────────
        self._output_box = customtkinter.CTkTextbox(
            center,
            font=customtkinter.CTkFont(family="Courier", size=14),
            border_spacing=14,
            state="disabled",
        )
        self._output_box.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        # ── row 7: error label ─────────────────────────────────────────
        self._error_label = customtkinter.CTkLabel(
            center,
            text="",
            text_color="#f38ba8",
            anchor="w",
            wraplength=580,
        )
        self._error_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))

    # ─────────────────────────── helpers ─────────────────────────────

    def _select_algo(self, name: str):
        """Highlight chosen sidebar button and update the title."""
        prev = self.selected_algo.get()
        self.selected_algo.set(name)

        if prev in self._algo_buttons:
            self._algo_buttons[prev].configure(
                fg_color="transparent",
                text_color=("gray10", "gray90"),
            )

        self._algo_buttons[name].configure(
            fg_color=("gray75", "gray25"),
            text_color=("gray10", "gray90"),
        )

        self._title_label.configure(text=name)

        if name == "Golomb":
            self._golomb_frame.grid()
            self._repetition_frame.grid_remove()
        elif name == "Repetição Ri":
            self._golomb_frame.grid_remove()
            self._repetition_frame.grid()
        else:
            self._golomb_frame.grid_remove()
            self._repetition_frame.grid_remove()

        self._clear_output()
        self._clear_error()
        self._send_btn.configure(state="disabled")
        self._last_server_payload = None
        self._server_status_label.configure(text="● Servidor: —", text_color="gray50")

        self._placeholder_active = False
        self._input_box.delete("1.0", "end")
        self._input_box.configure(text_color=("gray10", "gray90"))

        self._update_placeholder()

    def _on_operation_change(self):
        """Clear input whenever the user switches encode ↔ decode."""
        self._placeholder_active = False
        self._input_box.delete("1.0", "end")
        self._input_box.configure(text_color=("gray10", "gray90"))

        self._clear_output()
        self._clear_error()
        self._send_btn.configure(state="disabled")
        self._last_server_payload = None
        self._server_status_label.configure(text="● Servidor: —", text_color="gray50")

        if self.operation.get() == "encode":
            self._error_injection_frame.grid()
        else:
            self._error_injection_frame.grid_remove()

        self._update_placeholder()

    def _change_scaling(self, value: str):
        customtkinter.set_widget_scaling(int(value.replace("%", "")) / 100)
    
    def _apply_force_error(self, codeword: str) -> tuple[str, str | None]:
        """Return (final_codeword, corrupted_or_None).

        If no error indices are set, returns (codeword, None).
        Otherwise returns (corrupted, corrupted) — caller uses the second
        value to display the "with error" line.
        """
        indices = self._get_force_error_indices()
        if not indices:
            return codeword, None

        corrupted = self._inject_errors(codeword, indices)
        return corrupted, corrupted

    # ─────────────── placeholder helpers ─────────────────────────────

    def _needs_placeholder(self) -> bool:
        # Todos os modos devem ter placeholder, inclusive Huffman + Decodificar.
        return True

    def _get_placeholder_text(self) -> str:
        algo = self.selected_algo.get()
        mode = self.operation.get()

        if mode == "encode":
            if algo == "Huffman":
                return "Digite o texto a codificar. Exemplo: Água!"
            if algo in ("Repetição Ri", "Hamming (7,4)", "CRC-4"):
                return "Digite uma string binária. Exemplo: 10110100"

            return (
                "Digite números, texto ou símbolos separados por espaço/vírgula.\n"
                "Exemplo: 1 2 a b"
            )

        if mode == "decode":
            if algo == "Huffman":
                return (
                    "Digite o código binário seguido da tabela Huffman.\n"
                    "Exemplo: 1001011110100110 !:00, a:01, Á:100, g:101, @:110, u:111"
                )
            if algo in ("Repetição Ri", "Hamming (7,4)", "CRC-4"):
                return "Digite o código binário recebido. Exemplo: 000111000"

            return "Digite o código binário a decodificar. Exemplo: 001010111"

        return ""

    def _update_placeholder(self):
        """Show placeholder if the input box is empty and conditions are met."""
        if not self._needs_placeholder():
            return

        content = self._input_box.get("1.0", "end").strip()

        if not content:
            self._show_placeholder()

    def _show_placeholder(self):
        if not self._needs_placeholder():
            return

        placeholder = self._get_placeholder_text()

        if not placeholder:
            return

        self._input_box.delete("1.0", "end")
        self._input_box.insert("1.0", placeholder)
        self._input_box.configure(text_color="gray50")
        self._placeholder_active = True

    def _remove_placeholder(self):
        if self._placeholder_active:
            self._input_box.delete("1.0", "end")
            self._input_box.configure(text_color=("gray10", "gray90"))
            self._placeholder_active = False

    def _on_input_focus_in(self, _event=None):
        if self._placeholder_active:
            self._remove_placeholder()

    def _on_input_key_press(self, _event=None):
        if self._placeholder_active:
            self._remove_placeholder()

    def _on_input_focus_out(self, _event=None):
        content = self._input_box.get("1.0", "end").strip()

        if not content and self._needs_placeholder():
            self._show_placeholder()

    def _get_raw_input(self) -> str:
        """Return input text, treating active placeholder as empty."""
        if self._placeholder_active:
            return ""

        return self._input_box.get("1.0", "end").strip()
    
    # ─────────────────────────── submit ──────────────────────────────

    def _submit(self):
        self._clear_error()
        self._clear_output()

        raw = self._get_raw_input()
        if not raw:
            self._show_error("⚠  A entrada não pode estar vazia.")
            return

        algo = self.selected_algo.get()
        op   = self.operation.get()

        buf        = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf

        try:
            if op == "encode":
                self._run_encode(algo, raw)
            else:
                self._run_decode(algo, raw)
        except ValueError as exc:
            sys.stdout = old_stdout
            self._show_error(f"⚠  {exc}")
            return
        except Exception as exc:
            sys.stdout = old_stdout
            self._show_error(f"❌  Erro inesperado: {exc}")
            return
        finally:
            sys.stdout = old_stdout

        output_str = buf.getvalue().strip()
        self._set_output(output_str)

    def _get_force_error_indices(self) -> list[int]:
        error_raw = self._error_entry.get().strip()

        if not error_raw:
            return []

        try:
            indices = [int(x.strip()) for x in error_raw.split(",")]
        except ValueError as exc:
            raise ValueError(
                "Índices de erro inválidos. Use números inteiros separados por vírgula."
            ) from exc

        if any(idx < 0 for idx in indices):
            raise ValueError(
                "Os índices de erro devem ser inteiros maiores ou iguais a zero."
            )

        return indices

    def _inject_errors(self, string: str, indices: list[int]) -> str:
        char_list = list(string)
        bit_idx = 0
        for i, char in enumerate(char_list):
            if char in "01":
                if bit_idx in indices:
                    char_list[i] = "1" if char == "0" else "0"
                bit_idx += 1
        return "".join(char_list)

    # ─────────────── encode / decode dispatch ────────────────────────

    def _run_encode(self, algo: str, raw: str):
        if algo in ("Repetição Ri", "Hamming (7,4)", "CRC-4"):
            binary = raw.replace(" ", "")
            if not binary or not all(b in "01" for b in binary):
                raise ValueError("Entrada inválida — use apenas 0 e 1.")

            if algo == "Repetição Ri":
                r = self._get_r()
                result = repetition_encoder.encode(binary, r=r)
                codeword = result.encoded
                print(repetition_encoder.format_encode_result(result))

            elif algo == "Hamming (7,4)":
                result = hamming_encoder.encode(binary)
                codeword = result.encoded
                print(hamming_encoder.format_encode_result(result))

            elif algo == "CRC-4":
                result = crc_encoder.encode(binary)
                codeword = result.transmitted
                print(crc_encoder.format_encode_result(result))

            _, corrupted = self._apply_force_error(codeword)
            if corrupted is not None:
                print(f"\nCódigo original   : {codeword}")
                print(f"Código com erro   : {corrupted}")

            metadata = {"r": r} if algo == "Repetição Ri" else {}
            self._last_server_payload = (algo, codeword, metadata, self._get_force_error_indices())
            self.after(50, self._refresh_server_status)
            return

        if algo == "Huffman":
            result = huffman_encoder.encode(raw)
            codeword = result.encoded
            print(huffman_encoder.format_result(result))
            _, corrupted = self._apply_force_error(codeword)
            if corrupted is not None:
                print(f"\nCódigo original   : {codeword}")
                print(f"Código com erro   : {corrupted}")
            self._last_server_payload = (algo, codeword, {"code_table": result.code_table}, self._get_force_error_indices())
            self.after(50, self._refresh_server_status)
            return

        parsed = parse_integer_algorithm_input(raw, positive_only=True)
        numbers = parsed.numbers
        self._last_integer_metadata[algo] = parsed.metadata

        print(f"Tokens de entrada : {parsed.tokens}")
        print(format_input_metadata(parsed.metadata))

        if parsed.ascii_mapping:
            print(format_ascii_mapping(parsed.ascii_mapping))

        if algo == "Golomb":
            result = golomb_encoder.encode(numbers, m=self._get_m())
            print(golomb_encoder.format_result(result))

        elif algo == "Elias-Gamma":
            result = elias_gamma_encoder.encode(numbers)
            print(elias_gamma_encoder.format_result(result))

        elif algo == "Fibonacci/Zeckendorf":
            result = fibonacci_encoder.encode(numbers)
            print(fibonacci_encoder.format_result(result))

        codeword = result.encoded
        _, corrupted = self._apply_force_error(codeword)
        if corrupted is not None:
            print(f"\nCódigo original   : {codeword}")
            print(f"Código com erro   : {corrupted}")

        # payload: (algo, clean_codeword, metadata, error_indices)
        # clean_codeword is always the uncorrupted version so CRC can be
        # calculated correctly on the full transmitted frame before corruption.
        self._last_server_payload = (algo, codeword, {}, self._get_force_error_indices())
        self.after(50, self._refresh_server_status)

    def _update_server_status(self, online: bool):
        if online:
            self._server_status_label.configure(text="● Servidor: Online", text_color="#a6e3a1")
            if self._last_server_payload is not None:
                self._send_btn.configure(state="normal")
        else:
            self._server_status_label.configure(text="● Servidor: Offline", text_color="#f38ba8")
            self._send_btn.configure(state="disabled")

    def _refresh_server_status(self):
        from src.network.client import check_server  # lazy import
        self._update_server_status(check_server())

    _ERROR_ALGOS = {"Repetição Ri", "Hamming (7,4)", "CRC-4"}

    def _send_to_server(self):
        if self._last_server_payload is None:
            self._show_error("⚠  Nenhum codeword codificado para enviar.")
            return

        self._clear_error()
        self._send_btn.configure(state="disabled")

        algo, clean_codeword, metadata, error_indices = self._last_server_payload

        if algo not in self._ERROR_ALGOS:
            # Wrap the compression codeword with CRC so the server can detect errors.
            from src.algorithms.crc import encode as crc_encode  # lazy import
            crc_result = crc_encode(clean_codeword)
            transmitted = crc_result.transmitted
            send_algo = "CRC-4"
            send_metadata = {}
        else:
            transmitted = clean_codeword
            send_algo = algo
            send_metadata = metadata

        # Apply channel errors on the full transmitted frame (after CRC).
        if error_indices:
            transmitted = self._inject_errors(transmitted, error_indices)

        from src.network.client import send_codeword  # lazy import

        try:
            resp = send_codeword(send_algo, transmitted, send_metadata)
        except TimeoutError as exc:
            self._show_error(f"⚠  Sem resposta do servidor: {exc}")
            return
        except OSError as exc:
            self._show_error(f"❌  Erro de rede: {exc}")
            return
        except Exception as exc:
            self._show_error(f"❌  Erro inesperado: {exc}")
            return

        pos = resp["error_position"]
        if not resp["error_detected"]:
            erro_str = "Não detectado"
        elif pos is not None:
            erro_str = f"Posição {pos}"
        else:
            erro_str = "Detectado (posição não localizável pelo algoritmo)"
        server_block = (
            "\n"
            "── Servidor (127.0.0.1:9000) " + "─" * 40 + "\n"
            f"Enviado   : {transmitted}\n"
            f"Corrigido : {resp['corrected_codeword']}\n"
            f"Erro      : {erro_str}\n"
            f"Mensagem  : {resp['message']}\n"
            + "─" * 69
        )

        self._output_box.configure(state="normal")
        self._output_box.insert("end", server_block)
        self._output_box.see("end")
        self._output_box.configure(state="disabled")

    def _run_decode(self, algo: str, raw: str):
        if algo in ("Repetição Ri", "Hamming (7,4)", "CRC-4"):
            binary = raw.replace(" ", "")
            if not binary or not all(b in "01" for b in binary):
                raise ValueError("Entrada inválida — use apenas 0 e 1.")

            if algo == "Repetição Ri":
                r = self._get_r()
                result = repetition_encoder.decode(binary, r=r)
                print(repetition_encoder.format_decode_result(result))

            elif algo == "Hamming (7,4)":
                result = hamming_encoder.decode(binary)
                print(hamming_encoder.format_decode_result(result))

            elif algo == "CRC-4":
                result = crc_encoder.check(binary)
                print(crc_encoder.format_check_result(result))

            return

        if algo == "Huffman":
            binary, codes = parse_huffman_decode_input(raw)

            result = huffman_decoder.decode(binary, codes)
            print(huffman_decoder.format_decode_result(result))
            return

        binary = "".join(raw.split())

        if not binary:
            raise ValueError("Código binário vazio.")

        if not all(bit in "01" for bit in binary):
            raise ValueError("Código binário inválido — use apenas 0 e 1.")

        if algo == "Golomb":
            result = golomb_decoder.decode(binary, m=self._get_m())
            print(golomb_decoder.format_decode_result(result))

        elif algo == "Elias-Gamma":
            result = elias_gamma_decoder.decode(binary)
            print(elias_gamma_decoder.format_decode_result(result))

        elif algo == "Fibonacci/Zeckendorf":
            result = fibonacci_decoder.decode(binary)
            print(fibonacci_decoder.format_decode_result(result))

        metadata = self._last_integer_metadata.get(algo)
        print(format_reconstructed_decoding(result.numbers, metadata))

    # ─────────────────────────── utils ───────────────────────────────

    def _get_m(self) -> int:
        try:
            m = int(self.golomb_m.get())
            if m < 1:
                raise ValueError
            return m
        except ValueError as exc:
            raise ValueError("Parâmetro m deve ser um inteiro positivo.") from exc

    def _get_r(self) -> int:
        try:
            r = int(self.repetition_r.get())
            if r < 1:
                raise ValueError
            return r
        except ValueError as exc:
            raise ValueError("Parâmetro r deve ser um inteiro positivo.") from exc

    @staticmethod
    def _parse_numbers(raw: str, allow_zero: bool = False) -> list[int]:
        try:
            nums = [int(t) for t in raw.split()]
        except ValueError as exc:
            raise ValueError(
                "Entrada inválida — use números inteiros separados por espaço."
            ) from exc
        if allow_zero:
            if any(n < 0 for n in nums):
                raise ValueError("Este algoritmo requer números não-negativos (≥ 0).")
        else:
            if any(n <= 0 for n in nums):
                raise ValueError("Este algoritmo requer números positivos (> 0).")
        return nums

    def _set_output(self, text: str):
        self._output_box.configure(state="normal")
        self._output_box.delete("1.0", "end")
        self._output_box.insert("1.0", text)
        self._output_box.configure(state="disabled")

    def _clear_output(self):
        self._output_box.configure(state="normal")
        self._output_box.delete("1.0", "end")
        self._output_box.configure(state="disabled")

    def _show_error(self, msg: str):
        self._error_label.configure(text=msg)

    def _clear_error(self):
        self._error_label.configure(text="")


# ─────────────────────────── entry point ─────────────────────────────

def main():
    app = EncoderApp()
    app.mainloop()


if __name__ == "__main__":
    main()