import subprocess
import sys
from pathlib import Path

from scripts.package_windows import (
    DEFAULT_APP_NAME,
    DEFAULT_DIST_DIR,
    DEFAULT_SPEC_DIR,
    DEFAULT_WORK_DIR,
    ENTRY_SCRIPT,
    PROJECT_ROOT,
    TRACKED_SPEC_PATH,
    PackageWindowsOptions,
    build_pyinstaller_command,
    main,
)


def test_build_pyinstaller_command_uses_tracked_spec_by_default() -> None:
    command = build_pyinstaller_command(
        PackageWindowsOptions(
            app_name=DEFAULT_APP_NAME,
            mode="console",
            dist_dir=DEFAULT_DIST_DIR,
            work_dir=DEFAULT_WORK_DIR,
            spec_dir=DEFAULT_SPEC_DIR,
            spec_path=TRACKED_SPEC_PATH,
            use_spec=True,
            clean=True,
            noconfirm=True,
            dry_run=False,
        ),
    )

    assert command[:3] == [sys.executable, "-m", "PyInstaller"]
    assert command[-1] == str(TRACKED_SPEC_PATH)
    assert "--clean" in command
    assert "--noconfirm" in command
    assert "--console" not in command
    assert "build" in str(command)
    assert "dist" in str(command)


def test_build_pyinstaller_command_supports_generated_entrypoint_mode(tmp_path: Path) -> None:
    command = build_pyinstaller_command(
        PackageWindowsOptions(
            app_name="SnapLexPreview",
            mode="windowed",
            dist_dir=tmp_path / "dist",
            work_dir=tmp_path / "work",
            spec_dir=tmp_path / "spec",
            spec_path=TRACKED_SPEC_PATH,
            use_spec=False,
            clean=False,
            noconfirm=False,
            dry_run=False,
        ),
    )

    assert "SnapLexPreview" in command
    assert "--windowed" in command
    assert "--console" not in command
    assert "--clean" not in command
    assert "--noconfirm" not in command
    assert "--paths" in command
    assert str(PROJECT_ROOT) in command
    assert command[-1] == str(ENTRY_SCRIPT)


def test_package_windows_dry_run_prints_command(capsys) -> None:
    exit_code = main(["--dry-run", "--mode", "console"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "PyInstaller" in output
    assert subprocess.list2cmdline([str(TRACKED_SPEC_PATH)]) in output
