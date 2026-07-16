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
    parser.add_argument(
        "--check-real-provider",
        action="store_true",
        help="Check real-provider credential readiness without network calls.",
    )
    parser.add_argument(
        "--smoke-credentials",
        action="store_true",
        help="Run explicit credential-capable package smoke with a throwaway value.",
    )
    parser.add_argument(
        "--credential-smoke-mode",
        choices=("import", "cycle", "save", "check-delete"),
        default="cycle",
        help="Credential smoke mode for --smoke-credentials.",
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

    if args.check_real_provider:
        from snaplex.trial_readiness import check_real_provider_readiness

        result = check_real_provider_readiness()
        print(result.status_text)
        for line in result.detail_lines:
            print(f"- {line}")
        return 0 if result.ready else 1

    if args.smoke_credentials:
        from snaplex.release_smoke import PackagedSmokeError, run_packaged_credential_smoke

        try:
            smoke_lines = run_packaged_credential_smoke(mode=args.credential_smoke_mode)
        except PackagedSmokeError as exc:
            print(f"SnapLex packaged credential smoke FAIL: {exc}")
            return 1

        print("SnapLex packaged credential smoke PASS")
        for line in smoke_lines:
            print(f"- {line}")
        return 0

    return launch_gui()
