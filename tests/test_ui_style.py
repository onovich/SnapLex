import pytest

from snaplex.ui.style import (
    MIN_CONTRAST_RATIO,
    SNAPLEX_FONT_FAMILY,
    build_app_stylesheet,
    contrast_ratio,
    semantic_contrast_ratios,
)


def test_semantic_color_contrast_meets_accessible_baseline() -> None:
    ratios = semantic_contrast_ratios()

    assert ratios
    assert all(ratio >= MIN_CONTRAST_RATIO for ratio in ratios.values())


def test_stylesheet_names_font_focus_and_primary_action() -> None:
    stylesheet = build_app_stylesheet()

    assert SNAPLEX_FONT_FAMILY in stylesheet
    assert "QPushButton#PrimaryAction" in stylesheet
    assert "QPushButton:focus" in stylesheet
    assert "QLineEdit:focus" in stylesheet


def test_contrast_ratio_rejects_invalid_hex_color() -> None:
    with pytest.raises(ValueError):
        contrast_ratio("#fff", "#000000")
