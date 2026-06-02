"""
Utility functions for encoding algorithms.
"""

from src.utils.binary_utils import (
    binary_to_int,
    int_to_binary,
    binary_to_hex,
    hex_to_binary,
    format_binary,
)
from src.utils.validation import (
    validate_positive_int,
    validate_non_negative_int,
    validate_binary_string,
    validate_binary_string_decoder,
    validate_int_list,
    validate_text,
    validate_golomb_m,
    validate_repetition_r,
    validate_huffman_codes,
    validate_positive_numbers_input,
    validate_non_negative_numbers_input,
)

__all__ = [
    "binary_to_int",
    "int_to_binary",
    "binary_to_hex",
    "hex_to_binary",
    "format_binary",
    "validate_positive_int",
    "validate_non_negative_int",
    "validate_binary_string",
    "validate_binary_string_decoder",
    "validate_int_list",
    "validate_text",
    "validate_golomb_m",
    "validate_repetition_r",
    "validate_huffman_codes",
    "validate_positive_numbers_input",
    "validate_non_negative_numbers_input",
]