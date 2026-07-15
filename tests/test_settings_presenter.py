from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.services import (
    CredentialService,
    CredentialSource,
    CredentialStatusCode,
    InMemoryCredentialStore,
    SettingsService,
    keyring_credential_reference,
)
from snaplex.services.provider_setup import ProviderSetupStatus
from snaplex.storage import AppConfig, InMemoryConfigStore
from snaplex.ui.settings_presenter import SettingsFormState, SettingsPresenter


def test_settings_presenter_loads_form_state_from_config() -> None:
    store = InMemoryConfigStore(
        AppConfig(
            source_lang="ja",
            target_lang="en",
            provider_name="openai",
            provider_order=("openai", "fake"),
            provider_configs={
                "openai": ProviderRuntimeConfig(
                    base_url="https://api.openai.example/v1",
                    api_key_env_var="SNAPLEX_OPENAI_API_KEY",
                    credential_source="keyring",
                    credential_identifier="snaplex/openai/local",
                    timeout_seconds=4.0,
                    retry_count=2,
                    options={"model": "gpt-test"},
                )
            },
            history_enabled=True,
            history_max_entries=25,
        )
    )
    credential_store = InMemoryCredentialStore()
    credential_store.save(
        keyring_credential_reference("openai", "snaplex/openai/local"), "secret-value"
    )
    presenter = SettingsPresenter(
        SettingsService(
            store,
            credential_service=CredentialService({CredentialSource.KEYRING: credential_store}),
        )
    )

    state = presenter.load_state(environ={"SNAPLEX_OPENAI_API_KEY": "secret-value"})

    openai_setup = next(setup for setup in state.provider_setups if setup.provider_name == "openai")
    assert state.provider_choices == ("fake", "libretranslate", "openai", "deepl")
    assert state.source_lang == "ja"
    assert state.target_lang == "en"
    assert state.provider_name == "openai"
    assert state.provider_order == "openai, fake"
    assert state.openai_base_url == "https://api.openai.example/v1"
    assert state.openai_credential_source == "keyring"
    assert state.openai_credential_identifier == "snaplex/openai/local"
    assert state.openai_model == "gpt-test"
    assert openai_setup.status == ProviderSetupStatus.READY_FROM_KEYRING
    assert "secret-value" not in repr(state)
    assert state.history_enabled is True
    assert state.history_max_entries == 25


def test_settings_presenter_applies_form_state_to_service() -> None:
    store = InMemoryConfigStore()
    presenter = SettingsPresenter(SettingsService(store))

    state = presenter.apply_state(
        SettingsFormState(
            source_lang="fr",
            target_lang="en",
            provider_name="libretranslate",
            provider_order="libretranslate, fake",
            libretranslate_base_url="https://libre.example",
            libretranslate_api_key_env_var="SNAPLEX_LIBRE_KEY",
            libretranslate_timeout_seconds=3.0,
            libretranslate_retry_count=1,
            openai_model="gpt-test",
            openai_credential_source="keyring",
            openai_credential_identifier="snaplex/openai/local",
            history_enabled=True,
            history_max_entries=10,
        )
    )

    config = store.load()
    assert state.provider_name == "libretranslate"
    assert config.source_lang == "fr"
    assert config.target_lang == "en"
    assert config.provider_order == ("libretranslate", "fake")
    assert config.provider_configs["libretranslate"].base_url == "https://libre.example"
    assert config.provider_configs["libretranslate"].api_key_env_var == "SNAPLEX_LIBRE_KEY"
    assert config.provider_configs["libretranslate"].timeout_seconds == 3.0
    assert config.provider_configs["libretranslate"].retry_count == 1
    assert config.provider_configs["openai"].options["model"] == "gpt-test"
    assert config.provider_configs["openai"].credential_source == "keyring"
    assert config.provider_configs["openai"].credential_identifier == "snaplex/openai/local"
    assert config.history_enabled is True
    assert config.history_max_entries == 10


def test_settings_presenter_reports_missing_credentials_for_real_providers() -> None:
    presenter = SettingsPresenter(SettingsService(InMemoryConfigStore()))

    state = presenter.load_state(environ={})

    setup_by_name = {setup.provider_name: setup for setup in state.provider_setups}
    assert setup_by_name["fake"].status == ProviderSetupStatus.FAKE_SMOKE
    assert setup_by_name["libretranslate"].status == ProviderSetupStatus.READY_FROM_ENVIRONMENT
    assert setup_by_name["openai"].status == ProviderSetupStatus.MISSING_CREDENTIAL
    assert setup_by_name["deepl"].status == ProviderSetupStatus.MISSING_CREDENTIAL


def test_settings_presenter_saves_and_deletes_provider_credential_without_secret_repr() -> None:
    credential_store = InMemoryCredentialStore()
    store = InMemoryConfigStore()
    presenter = SettingsPresenter(
        SettingsService(
            store,
            credential_service=CredentialService({CredentialSource.KEYRING: credential_store}),
        )
    )
    presenter.update_provider_credential_reference(
        "openai",
        credential_source="keyring",
        credential_identifier="snaplex/openai/local",
    )

    saved = presenter.save_provider_credential("openai", "secret-value")
    deleted = presenter.delete_provider_credential("openai")

    assert saved.code == CredentialStatusCode.SAVED
    assert deleted.code == CredentialStatusCode.DELETED
    assert "secret-value" not in repr(saved)
    assert "secret-value" not in repr(store.load())
