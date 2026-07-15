from snaplex.app import main
from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.services import (
    CredentialService,
    CredentialSource,
    InMemoryCredentialStore,
    keyring_credential_reference,
)
from snaplex.storage import APP_DATA_DIR_ENV_VAR, AppConfig
from snaplex.trial_readiness import check_real_provider_readiness


def test_cli_check_real_provider_rejects_missing_configuration(
    monkeypatch,
    tmp_path,
    capsys,
) -> None:
    monkeypatch.setenv(APP_DATA_DIR_ENV_VAR, str(tmp_path))
    monkeypatch.delenv("SNAPLEX_PROVIDER", raising=False)
    monkeypatch.delenv("SNAPLEX_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("SNAPLEX_DEEPL_API_KEY", raising=False)
    monkeypatch.delenv("SNAPLEX_LIBRETRANSLATE_BASE_URL", raising=False)

    exit_code = main(["--check-real-provider"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Real translation provider is not configured" in output


def test_cli_check_real_provider_accepts_existing_env_var(
    monkeypatch,
    tmp_path,
    capsys,
) -> None:
    monkeypatch.setenv(APP_DATA_DIR_ENV_VAR, str(tmp_path))
    monkeypatch.setenv("SNAPLEX_OPENAI_API_KEY", "secret-value")

    exit_code = main(["--check-real-provider"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Real provider ready: OpenAI" in output
    assert "secret-value" not in output


def test_trial_readiness_accepts_configured_keyring_store_without_real_keyring() -> None:
    credential_store = InMemoryCredentialStore()
    credential_store.save(keyring_credential_reference("openai"), "secret-value")

    result = check_real_provider_readiness(
        environ={},
        config=AppConfig(
            provider_name="openai",
            provider_order=("openai",),
            provider_configs={
                "openai": ProviderRuntimeConfig(credential_source="keyring"),
            },
        ),
        credential_service=CredentialService({CredentialSource.KEYRING: credential_store}),
    )

    assert result.ready is True
    assert result.provider_name == "openai"
    assert "secret-value" not in repr(result)


def test_trial_readiness_rejects_missing_keyring_secret() -> None:
    result = check_real_provider_readiness(
        environ={},
        config=AppConfig(
            provider_name="openai",
            provider_order=("openai",),
            provider_configs={
                "openai": ProviderRuntimeConfig(credential_source="keyring"),
            },
        ),
        credential_service=CredentialService(
            {CredentialSource.KEYRING: InMemoryCredentialStore()},
        ),
    )

    assert result.ready is False
    assert result.provider_name == ""
    assert any("Credential missing" in line for line in result.detail_lines)
