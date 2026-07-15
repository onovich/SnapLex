"""P11 visible Windows Qt-platform GUI smoke helper.

The helper opens real Qt windows using the native Windows platform plugin,
captures ignored local screenshots, and exits by timer. It is intentionally
separate from app bootstrap so release-hardening evidence does not move product
rules into smoke scripts.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCENARIOS = (
    "idle",
    "fake-success",
    "long-small",
    "settings",
    "history-empty",
    "focus",
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=SCENARIOS)
    parser.add_argument("--output-dir", default="snaplex-smoke-data/p11-visible-screenshots")
    parser.add_argument(
        "--platform",
        default="windows" if os.name == "nt" else "",
        help="Qt platform plugin to use. Defaults to windows on Windows.",
    )
    args = parser.parse_args(argv)

    if args.scenario:
        return _run_one(args.scenario, Path(args.output_dir), args.platform)

    output_dir = Path(args.output_dir)
    for scenario in SCENARIOS:
        command = [
            sys.executable,
            __file__,
            "--scenario",
            scenario,
            "--output-dir",
            str(output_dir),
        ]
        if args.platform:
            command.extend(["--platform", args.platform])
        try:
            subprocess.run(command, check=True, timeout=25)
        except subprocess.TimeoutExpired:
            print(f"P11 visible GUI smoke BLOCKED: {scenario} timed out.")
            return 2
        except subprocess.CalledProcessError as exc:
            print(f"P11 visible GUI smoke BLOCKED: {scenario} exited {exc.returncode}.")
            return exc.returncode
    print(f"P11 visible GUI smoke PASS: {len(SCENARIOS)} screenshots in {output_dir}")
    return 0


def _run_one(scenario: str, output_dir: Path, platform: str) -> int:
    if platform:
        os.environ["QT_QPA_PLATFORM"] = platform
    os.environ.setdefault("SNAPLEX_APP_DATA_DIR", str(Path("snaplex-smoke-data/p11-app-data")))

    from PySide6.QtCore import QTimer
    from PySide6.QtGui import QFontDatabase
    from PySide6.QtWidgets import QApplication

    from snaplex.ui.app_shell import launch_gui
    from snaplex.ui.clipboard_presenter import ClipboardTranslationPresenter

    app = QApplication.instance() or QApplication([])
    font_count = len(QFontDatabase.families())
    if font_count <= 0:
        raise AssertionError("Visible Windows smoke requires at least one desktop font family.")

    presenter = ClipboardTranslationPresenter()
    if scenario == "fake-success":
        presenter.show_success(
            source_text="hello",
            translated_text="hello [zh]",
            provider_name="fake",
        )
    elif scenario == "long-small":
        presenter.show_success(
            source_text="Long source text " * 80,
            translated_text="Long translated text " * 90,
            provider_name="fake",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{scenario}.png"

    if scenario == "settings":
        QTimer.singleShot(220, lambda: _click_accessible(app, "Open Settings"))
        QTimer.singleShot(
            800,
            lambda: _grab_assert_and_close(
                app,
                "SnapLex Settings",
                output_path,
                required_text=("Provider Setup", "Credential", "Connect account"),
            ),
        )
    elif scenario == "history-empty":
        QTimer.singleShot(220, lambda: _click_accessible(app, "Open History"))
        QTimer.singleShot(
            800,
            lambda: _grab_assert_and_close(
                app,
                "SnapLex History",
                output_path,
                required_text=("Enable history", "Close"),
            ),
        )
    elif scenario == "focus":
        QTimer.singleShot(250, lambda: _focus_accessible(app, "Translate clipboard text"))
        QTimer.singleShot(
            500,
            lambda: _grab_assert_and_close(
                app,
                "SnapLex",
                output_path,
                required_text=("SnapLex", "Translate Clipboard", "Translate Screen"),
                required_focus="Translate clipboard text",
            ),
        )
    elif scenario == "fake-success":
        QTimer.singleShot(
            400,
            lambda: _grab_assert_and_close(
                app,
                "SnapLex",
                output_path,
                required_text=("Fake smoke mode", "Provider: fake", "hello [zh]"),
            ),
        )
    else:
        resize = (390, 420) if scenario == "long-small" else None
        required_text = (
            ("Long source text", "Long translated text")
            if scenario == "long-small"
            else ("SnapLex", "Ready")
        )
        QTimer.singleShot(
            400,
            lambda: _grab_assert_and_close(
                app,
                "SnapLex",
                output_path,
                resize=resize,
                required_text=required_text,
            ),
        )

    return launch_gui(presenter=presenter)


def _click_accessible(app: Any, accessible_name: str) -> None:
    _widget_by_accessible_name(app, accessible_name).click()


def _focus_accessible(app: Any, accessible_name: str) -> None:
    widget = _widget_by_accessible_name(app, accessible_name)
    widget.setFocus()


def _widget_by_accessible_name(app: Any, accessible_name: str) -> Any:
    return next(
        widget
        for widget in app.allWidgets()
        if hasattr(widget, "accessibleName") and widget.accessibleName() == accessible_name
    )


def _grab_assert_and_close(
    app: Any,
    window_title: str,
    output_path: Path,
    *,
    resize: tuple[int, int] | None = None,
    required_text: tuple[str, ...] = (),
    required_focus: str = "",
) -> None:
    window = next(
        widget
        for widget in app.topLevelWidgets()
        if widget.isVisible() and widget.windowTitle() == window_title
    )
    if resize is not None:
        window.resize(*resize)
    for text in required_text:
        _assert_window_text(app, text)
    if required_focus:
        focus_widget = app.focusWidget()
        focus_name = focus_widget.accessibleName() if focus_widget is not None else ""
        if focus_name != required_focus:
            raise AssertionError(f"Expected focus {required_focus!r}, got {focus_name!r}")

    image = window.grab().toImage()
    _assert_nonblank(image, window_title)
    if not image.save(str(output_path)):
        raise AssertionError(f"Could not save screenshot: {output_path}")
    print(f"{window_title}: saved {output_path} {image.width()}x{image.height()}")
    window.close()
    app.quit()


def _assert_window_text(app: Any, expected_text: str) -> None:
    haystack = "\n".join(_widget_text(widget) for widget in app.allWidgets())
    if expected_text not in haystack:
        raise AssertionError(f"Expected visible text not found: {expected_text!r}")


def _widget_text(widget: Any) -> str:
    if hasattr(widget, "text"):
        try:
            return str(widget.text())
        except TypeError:
            return ""
    if hasattr(widget, "toPlainText"):
        return str(widget.toPlainText())
    return ""


def _assert_nonblank(image: Any, label: str) -> None:
    if image.isNull():
        raise AssertionError(f"{label} screenshot is null")
    if image.width() < 300 or image.height() < 250:
        raise AssertionError(f"{label} screenshot is too small: {image.width()}x{image.height()}")
    x_step = max(1, image.width() // 4)
    y_step = max(1, image.height() // 4)
    sampled_colors = {
        image.pixelColor(x, y).rgba()
        for x in range(0, image.width(), x_step)
        for y in range(0, image.height(), y_step)
    }
    if len(sampled_colors) < 2:
        raise AssertionError(f"{label} screenshot appears blank")


if __name__ == "__main__":
    raise SystemExit(main())
