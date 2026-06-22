"""Build a local Windows SnapLex package with PyInstaller.

The script is intentionally a thin packaging wrapper: application bootstrap,
provider selection, settings, history, capture, and OCR behavior stay inside the
SnapLex package.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_NAME = "SnapLex"
DEFAULT_DIST_DIR = PROJECT_ROOT / "dist"
DEFAULT_WORK_DIR = PROJECT_ROOT / "build" / "pyinstaller"
DEFAULT_SPEC_DIR = PROJECT_ROOT / "build" / "pyinstaller" / "spec"
TRACKED_SPEC_PATH = PROJECT_ROOT / "packaging" / "snaplex.spec"
ENTRY_SCRIPT = PROJECT_ROOT / "snaplex" / "__main__.py"


@dataclass(frozen=True)
class PackageWindowsOptions:
    app_name: str
    mode: str
    dist_dir: Path
    work_dir: Path
    spec_dir: Path
    spec_path: Path
    use_spec: bool
    clean: bool
    noconfirm: bool
    dry_run: bool


def build_pyinstaller_command(options: PackageWindowsOptions) -> list[str]:
    """Return the PyInstaller command for the current source checkout."""

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--distpath",
        str(options.dist_dir),
        "--workpath",
        str(options.work_dir),
    ]
    if options.clean:
        command.append("--clean")
    if options.noconfirm:
        command.append("--noconfirm")
    if options.use_spec:
        command.append(str(options.spec_path))
        return command

    command.extend(
        [
            "--name",
            options.app_name,
            "--specpath",
            str(options.spec_dir),
            "--paths",
            str(PROJECT_ROOT),
        ]
    )
    command.append("--windowed" if options.mode == "windowed" else "--console")
    command.append(str(ENTRY_SCRIPT))
    return command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the SnapLex Windows package with PyInstaller.",
    )
    parser.add_argument("--name", default=DEFAULT_APP_NAME, help="Packaged application name.")
    parser.add_argument(
        "--mode",
        choices=("console", "windowed"),
        default="console",
        help="Use console mode for repeatable smoke output or windowed mode for GUI-only launch.",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=DEFAULT_DIST_DIR,
        help="Generated distribution directory.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=DEFAULT_WORK_DIR,
        help="Generated PyInstaller work directory.",
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=DEFAULT_SPEC_DIR,
        help="Directory for generated throwaway PyInstaller spec files.",
    )
    parser.add_argument(
        "--spec-path",
        type=Path,
        default=TRACKED_SPEC_PATH,
        help="Tracked PyInstaller spec path used by default.",
    )
    parser.add_argument(
        "--no-spec",
        action="store_true",
        help="Generate a temporary spec from command-line options instead of using packaging/snaplex.spec.",
    )
    parser.add_argument("--no-clean", action="store_true", help="Skip PyInstaller --clean.")
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip PyInstaller --noconfirm.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the PyInstaller command without executing it.",
    )
    return parser


def options_from_args(args: argparse.Namespace) -> PackageWindowsOptions:
    return PackageWindowsOptions(
        app_name=args.name,
        mode=args.mode,
        dist_dir=args.dist_dir,
        work_dir=args.work_dir,
        spec_dir=args.spec_dir,
        spec_path=args.spec_path,
        use_spec=not args.no_spec,
        clean=not args.no_clean,
        noconfirm=not args.no_confirm,
        dry_run=args.dry_run,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = options_from_args(parser.parse_args(argv))
    if options.use_spec and not options.spec_path.exists():
        print(f"PyInstaller spec not found: {options.spec_path}", file=sys.stderr)
        return 1

    command = build_pyinstaller_command(options)
    print(subprocess.list2cmdline(command))
    if options.dry_run:
        return 0

    try:
        result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    except FileNotFoundError:
        print(
            'PyInstaller is not installed. Run: python -m pip install -e ".[package]"',
            file=sys.stderr,
        )
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
