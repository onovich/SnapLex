from snaplex.app import main
from snaplex.release_smoke import (
    CREDENTIAL_SMOKE_IDENTIFIER,
    PackagedSmokeError,
    run_packaged_credential_smoke,
    run_packaged_workflow_smoke,
)
from snaplex.storage import APP_DATA_DIR_ENV_VAR, CONFIG_FILE_NAME, HISTORY_FILE_NAME


class FakeCredentialSmokeBackend:
    pass


class FakeCredentialSmokeKeyring:
    def __init__(self) -> None:
        self._passwords: dict[tuple[str, str], str] = {}

    def get_keyring(self) -> FakeCredentialSmokeBackend:
        return FakeCredentialSmokeBackend()

    def get_password(self, service_name: str, username: str) -> str | None:
        return self._passwords.get((service_name, username))

    def set_password(self, service_name: str, username: str, password: str) -> None:
        self._passwords[(service_name, username)] = password

    def delete_password(self, service_name: str, username: str) -> None:
        self._passwords.pop((service_name, username), None)


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


def test_packaged_credential_import_smoke_uses_keyring_boundary() -> None:
    smoke_lines = run_packaged_credential_smoke(
        mode="import",
        keyring_module=FakeCredentialSmokeKeyring(),
    )

    output = "\n".join(smoke_lines)
    assert "keyring import/backend discovery: PASS" in output
    assert CREDENTIAL_SMOKE_IDENTIFIER in output
    assert "credential value" not in output.lower()


def test_packaged_credential_cycle_smoke_cleans_up_without_leaking_secret() -> None:
    keyring_module = FakeCredentialSmokeKeyring()

    smoke_lines = run_packaged_credential_smoke(mode="cycle", keyring_module=keyring_module)

    output = "\n".join(smoke_lines)
    assert "credential save/read/delete: PASS" in output
    assert "credential cleanup: PASS" in output
    assert "credential value" not in output.lower()
    assert keyring_module._passwords == {}


def test_packaged_credential_restart_smoke_modes_share_reference_without_leak() -> None:
    keyring_module = FakeCredentialSmokeKeyring()

    save_lines = run_packaged_credential_smoke(mode="save", keyring_module=keyring_module)
    check_lines = run_packaged_credential_smoke(
        mode="check-delete",
        keyring_module=keyring_module,
    )

    output = "\n".join((*save_lines, *check_lines))
    assert "credential save: PASS" in output
    assert "credential restart readiness: PASS" in output
    assert "credential cleanup: PASS" in output
    assert "credential value" not in output.lower()
    assert keyring_module._passwords == {}


def test_cli_packaged_credential_import_smoke(capsys) -> None:
    exit_code = main(["--smoke-credentials", "--credential-smoke-mode", "import"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "SnapLex packaged credential smoke PASS" in output
    assert "keyring import/backend discovery: PASS" in output
    assert "credential value" not in output.lower()
