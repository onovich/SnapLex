"""Application bootstrap for SnapLex."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from snaplex import __version__
from snaplex.ui.app_shell import is_pyside_available, launch_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="snaplex", description="SnapLex desktop bootstrap.")
    parser.add_argument("--version", action="store_true", help="Print the SnapLex version.")
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Validate the bootstrap without starting the desktop shell.",
    )
    parser.add_argument(
        "--smoke-package",
        action="store_true",
        help="Run deterministic packaged workflow smoke using SNAPLEX_APP_DATA_DIR.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"SnapLex {__version__}")
        return 0

    if args.no_gui:
        gui_state = "available" if is_pyside_available() else "not installed"
        print(f"SnapLex bootstrap OK (PySide6 {gui_state}).")
        return 0

    if args.smoke_package:
        from snaplex.release_smoke import PackagedSmokeError, run_packaged_workflow_smoke

        try:
            smoke_lines = run_packaged_workflow_smoke()
        except PackagedSmokeError as exc:
            print(f"SnapLex packaged workflow smoke FAIL: {exc}")
            return 1

        print("SnapLex packaged workflow smoke PASS")
        for line in smoke_lines:
            print(f"- {line}")
        return 0

    return launch_gui()
