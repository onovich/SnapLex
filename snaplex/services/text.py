"""Text normalization helpers shared by OCR and clipboard flows."""

from __future__ import annotations


def _collapse_inline_whitespace(text: str) -> str:
    return " ".join(text.split())


def normalize_text(text: str) -> str:
    normalized_newlines = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized_lines = [
        _collapse_inline_whitespace(line.strip()) for line in normalized_newlines.split("\n")
    ]
    return "\n".join(line for line in normalized_lines if line).strip()
