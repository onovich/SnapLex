"""P9 offscreen GUI screenshot smoke helper."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCENARIOS = (
    "idle",
    "loading",
    "fake-success",
    "error",
    "long-small",
    "settings",
    "history-empty",
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=SCENARIOS)
    parser.add_argument("--output-dir", default="snaplex-smoke-data/p9-screenshots")
    args = parser.parse_args(argv)

    if args.scenario:
        return _run_one(args.scenario, Path(args.output_dir))

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
        subprocess.run(command, check=True)
    print(f"P9 GUI smoke PASS: {len(SCENARIOS)} screenshots in {output_dir}")
    return 0


def _run_one(scenario: str, output_dir: Path) -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("SNAPLEX_APP_DATA_DIR", str(Path("snaplex-smoke-data/p9-app-data")))

    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication

    from snaplex.ui.app_shell import launch_gui
    from snaplex.ui.clipboard_presenter import ClipboardTranslationPresenter

    app = QApplication.instance() or QApplication([])
    presenter = ClipboardTranslationPresenter()
    if scenario == "loading":
        presenter.request_translation(source_text="Loading source text")
    elif scenario == "fake-success":
        presenter.show_success(
            source_text="hello",
            translated_text="hello [zh]",
            provider_name="fake",
        )
    elif scenario == "error":
        presenter.show_error("Translation timed out. Try again.", source_text="hello")
    elif scenario == "long-small":
        presenter.show_success(
            source_text="Long source text " * 80,
            translated_text="Long translated text " * 90,
            provider_name="fake",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{scenario}.png"

    if scenario == "settings":
        QTimer.singleShot(180, lambda: _click_accessible(app, "Open Settings"))
        QTimer.singleShot(
            650,
            lambda: _grab_and_close(app, "SnapLex Settings", output_dir / filename),
        )
    elif scenario == "history-empty":
        QTimer.singleShot(180, lambda: _click_accessible(app, "Open History"))
        QTimer.singleShot(
            650,
            lambda: _grab_and_close(app, "SnapLex History", output_dir / filename),
        )
    else:
        resize = (390, 420) if scenario == "long-small" else None
        QTimer.singleShot(
            250,
            lambda: _grab_and_close(app, "SnapLex", output_dir / filename, resize=resize),
        )

    return launch_gui(presenter=presenter)


def _click_accessible(app: Any, accessible_name: str) -> None:
    widget = next(
        widget
        for widget in app.allWidgets()
        if hasattr(widget, "accessibleName") and widget.accessibleName() == accessible_name
    )
    widget.click()


def _grab_and_close(
    app: Any,
    window_title: str,
    output_path: Path,
    *,
    resize: tuple[int, int] | None = None,
) -> None:
    window = next(
        widget
        for widget in app.topLevelWidgets()
        if widget.isVisible() and widget.windowTitle() == window_title
    )
    if resize is not None:
        window.resize(*resize)
    image = window.grab().toImage()
    _assert_nonblank(image, window_title)
    if not image.save(str(output_path)):
        raise AssertionError(f"Could not save screenshot: {output_path}")
    print(f"{window_title}: saved {output_path} {image.width()}x{image.height()}")
    window.close()
    app.quit()


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
