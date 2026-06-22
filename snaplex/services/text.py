"""Text normalization helpers shared by OCR and clipboard flows."""

from __future__ import annotations


def normalize_text(text: str) -> str:
    normalized_newlines = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.strip() for line in normalized_newlines.split("\n")).strip()
