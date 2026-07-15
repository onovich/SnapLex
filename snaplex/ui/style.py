"""Shared visual tokens for the SnapLex PySide6 shell."""

from __future__ import annotations

from dataclasses import dataclass


SNAPLEX_FONT_FAMILY = "Segoe UI"
MIN_CONTRAST_RATIO = 4.5


@dataclass(frozen=True)
class UiColor:
    name: str
    value: str


BACKGROUND = UiColor("background", "#f7f8f6")
SURFACE = UiColor("surface", "#ffffff")
SUBTLE_SURFACE = UiColor("subtle_surface", "#fbfcfb")
TEXT = UiColor("text", "#1f2933")
TEXT_STRONG = UiColor("text_strong", "#101828")
TEXT_MUTED = UiColor("text_muted", "#5f6b7a")
BORDER = UiColor("border", "#d8dee6")
BORDER_STRONG = UiColor("border_strong", "#c7d0da")
FOCUS = UiColor("focus", "#1457c4")
PRIMARY = UiColor("primary", "#1f6feb")
PRIMARY_TEXT = UiColor("primary_text", "#ffffff")
WARNING_BG = UiColor("warning_bg", "#fff4d6")
WARNING_BORDER = UiColor("warning_border", "#f0c36a")
WARNING_TEXT = UiColor("warning_text", "#6b4b00")
ERROR_TEXT = UiColor("error_text", "#b42318")
DISABLED_TEXT = UiColor("disabled_text", "#5f6b7a")
DISABLED_BG = UiColor("disabled_bg", "#eef1f4")


SPACING_1 = 6
SPACING_2 = 10
SPACING_3 = 14
SPACING_4 = 18
CONTROL_MIN_HEIGHT = 32
BORDER_RADIUS = 6


def build_app_stylesheet() -> str:
    return f"""
        QWidget {{
            color: {TEXT.value};
            font-family: "{SNAPLEX_FONT_FAMILY}";
            font-size: 13px;
        }}
        QWidget#SnapLexRoot, QDialog {{
            background: {BACKGROUND.value};
        }}
        QLabel#AppTitle {{
            font-size: 22px;
            font-weight: 700;
            color: {TEXT_STRONG.value};
        }}
        QLabel#AppSubtitle, QLabel#SectionLabel {{
            color: {TEXT_MUTED.value};
        }}
        QLabel#ResultText {{
            background: {SURFACE.value};
            border: 1px solid {BORDER.value};
            border-radius: {BORDER_RADIUS}px;
            padding: 8px;
            min-height: 36px;
        }}
        QLabel#ProviderText {{
            color: #344054;
            font-weight: 600;
        }}
        QLabel#ProviderNotice {{
            background: {WARNING_BG.value};
            border: 1px solid {WARNING_BORDER.value};
            border-radius: {BORDER_RADIUS}px;
            color: {WARNING_TEXT.value};
            padding: {SPACING_1}px;
        }}
        QLabel#ErrorText {{
            color: {ERROR_TEXT.value};
            font-weight: 600;
        }}
        QLabel#StatusText {{
            color: {TEXT_MUTED.value};
        }}
        QLabel#StatusPill {{
            background: {SURFACE.value};
            border: 1px solid {BORDER.value};
            border-radius: 12px;
            color: {TEXT_MUTED.value};
            padding: 4px 10px;
            min-height: 24px;
        }}
        QLabel#StatusPill[resultState="loading"],
        QLabel#ResultStateBadge[resultState="loading"] {{
            background: #eef4ff;
            border-color: #9db7ff;
            color: #173b85;
        }}
        QLabel#StatusPill[resultState="success"],
        QLabel#ResultStateBadge[resultState="success"] {{
            background: #eaf7ef;
            border-color: #9bd3ad;
            color: #166534;
        }}
        QLabel#StatusPill[resultState="empty"],
        QLabel#StatusPill[resultState="cancelled"],
        QLabel#ResultStateBadge[resultState="empty"],
        QLabel#ResultStateBadge[resultState="cancelled"] {{
            background: {WARNING_BG.value};
            border-color: {WARNING_BORDER.value};
            color: {WARNING_TEXT.value};
        }}
        QLabel#StatusPill[resultState="error"],
        QLabel#ResultStateBadge[resultState="error"] {{
            background: #fff1f0;
            border-color: #f2aaa5;
            color: {ERROR_TEXT.value};
        }}
        QLabel#ResultStateBadge {{
            background: {SURFACE.value};
            border: 1px solid {BORDER.value};
            border-radius: 10px;
            color: {TEXT_MUTED.value};
            font-weight: 600;
            padding: 4px 8px;
        }}
        QGroupBox {{
            border: 1px solid {BORDER.value};
            border-radius: 8px;
            margin-top: {SPACING_2}px;
            padding: {SPACING_2}px 8px 8px 8px;
            background: {SUBTLE_SURFACE.value};
            font-weight: 600;
        }}
        QPushButton, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            min-height: {CONTROL_MIN_HEIGHT}px;
            border-radius: {BORDER_RADIUS}px;
            border: 1px solid {BORDER_STRONG.value};
            background: {SURFACE.value};
        }}
        QPushButton {{
            padding: 6px 10px;
        }}
        QPushButton#PrimaryAction {{
            background: {PRIMARY.value};
            border-color: {PRIMARY.value};
            color: {PRIMARY_TEXT.value};
            font-weight: 600;
        }}
        QPushButton#SecondaryAction {{
            background: {SUBTLE_SURFACE.value};
        }}
        QPushButton#ResultAction {{
            min-width: 96px;
        }}
        QPushButton:disabled {{
            color: {DISABLED_TEXT.value};
            background: {DISABLED_BG.value};
        }}
        QPushButton:focus,
        QLineEdit:focus,
        QComboBox:focus,
        QSpinBox:focus,
        QDoubleSpinBox:focus,
        QListWidget:focus {{
            border: 2px solid {FOCUS.value};
        }}
        QListWidget {{
            background: {SURFACE.value};
            border: 1px solid {BORDER.value};
            border-radius: {BORDER_RADIUS}px;
        }}
    """


def contrast_ratio(foreground: str, background: str) -> float:
    foreground_luminance = _relative_luminance(foreground)
    background_luminance = _relative_luminance(background)
    lighter = max(foreground_luminance, background_luminance)
    darker = min(foreground_luminance, background_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def semantic_contrast_ratios() -> dict[str, float]:
    return {
        "text_on_background": contrast_ratio(TEXT.value, BACKGROUND.value),
        "strong_text_on_background": contrast_ratio(TEXT_STRONG.value, BACKGROUND.value),
        "primary_text_on_primary": contrast_ratio(PRIMARY_TEXT.value, PRIMARY.value),
        "warning_text_on_warning": contrast_ratio(WARNING_TEXT.value, WARNING_BG.value),
        "error_text_on_background": contrast_ratio(ERROR_TEXT.value, BACKGROUND.value),
        "disabled_text_on_disabled": contrast_ratio(DISABLED_TEXT.value, DISABLED_BG.value),
    }


def _relative_luminance(hex_color: str) -> float:
    red, green, blue = _hex_to_rgb(hex_color)
    values = []
    for channel in (red, green, blue):
        channel_value = channel / 255
        if channel_value <= 0.03928:
            values.append(channel_value / 12.92)
        else:
            values.append(((channel_value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.removeprefix("#")
    if len(value) != 6:
        raise ValueError(f"Expected 6-digit hex color, got {hex_color!r}.")
    return (
        int(value[0:2], 16),
        int(value[2:4], 16),
        int(value[4:6], 16),
    )
