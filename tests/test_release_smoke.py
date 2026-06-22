from snaplex.app import main
from snaplex.release_smoke import PackagedSmokeError, run_packaged_workflow_smoke
from snaplex.storage import APP_DATA_DIR_ENV_VAR, CONFIG_FILE_NAME, HISTORY_FILE_NAME


def test_packaged_workflow_smoke_requires_app_data_override(monkeypatch) -> None:
    monkeypatch.delenv(APP_DATA_DIR_ENV_VAR, raising=False)

    try:
        run_packaged_workflow_smoke()
    except PackagedSmokeError as exc:
        assert APP_DATA_DIR_ENV_VAR in str(exc)
    else:
        raise AssertionError("Expected PackagedSmokeError")


def test_packaged_workflow_smoke_uses_local_app_data(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(APP_DATA_DIR_ENV_VAR, str(tmp_path))

    smoke_lines = run_packaged_workflow_smoke()

    assert (tmp_path / CONFIG_FILE_NAME).exists()
    assert (tmp_path / HISTORY_FILE_NAME).exists()
    assert any("clipboard translation" in line for line in smoke_lines)
    assert any("screen fake capture/OCR translation" in line for line in smoke_lines)
    assert "secret" not in (tmp_path / CONFIG_FILE_NAME).read_text(encoding="utf-8").lower()


def test_cli_packaged_workflow_smoke(monkeypatch, tmp_path, capsys) -> None:
    monkeypatch.setenv(APP_DATA_DIR_ENV_VAR, str(tmp_path))

    exit_code = main(["--smoke-package"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "SnapLex packaged workflow smoke PASS" in output
    assert str(tmp_path) in output
