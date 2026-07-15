from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.services import SettingsService
from snaplex.services.provider_setup import ProviderSetupStatus
from snaplex.storage import AppConfig, InMemoryConfigStore


def test_settings_service_updates_language_defaults() -> None:
    store = InMemoryConfigStore()
    service = SettingsService(store)

    config = service.update_language_defaults(source_lang="ja", target_lang="en")

    assert config.source_lang == "ja"
    assert config.target_lang == "en"
    assert store.load().source_lang == "ja"


def test_settings_service_updates_provider_selection() -> None:
    store = InMemoryConfigStore()
    service = SettingsService(store)

    config = service.update_provider_selection(
        provider_name="libretranslate",
        provider_order="libretranslate, fake",
    )

    assert config.provider_name == "libretranslate"
    assert config.provider_order == ("libretranslate", "fake")


def test_settings_service_loads_provider_setup_states_without_secret_values() -> None:
    store = InMemoryConfigStore(
        AppConfig(
            provider_configs={
                "openai": ProviderRuntimeConfig(api_key_env_var="OPENAI_API_KEY"),
            },
        )
    )
    service = SettingsService(store)

    states = service.load_provider_setup_states(environ={"OPENAI_API_KEY": "secret-value"})

    openai_state = next(state for state in states if state.provider_name == "openai")
    assert openai_state.status == ProviderSetupStatus.READY_FROM_ENVIRONMENT
    assert openai_state.api_key_present is True
    assert "secret-value" not in repr(states)


def test_settings_service_connection_test_returns_provider_result() -> None:
    class TestTransport:
        def send(self, request: object) -> object:
            from snaplex.providers.http import HttpResponse

            return HttpResponse(200, b'{"translatedText":"hola"}')

    store = InMemoryConfigStore(
        AppConfig(
            provider_configs={
                "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example"),
            },
        )
    )
    service = SettingsService(store)

    result = service.test_provider_connection("libretranslate", http_transport=TestTransport())

    assert result.status == ProviderSetupStatus.TEST_PASSED
    assert result.translated_text == "hola"


def test_settings_service_updates_provider_runtime_config_without_secret_values() -> None:
    store = InMemoryConfigStore()
    service = SettingsService(store)

    config = service.update_provider_runtime_config(
        "openai",
        base_url="https://api.openai.example/v1",
        api_key_env_var="MY_OPENAI_KEY",
        timeout_seconds="4.5",
        retry_count="2",
        options={"model": "gpt-test", "unused": ""},
    )

    openai_config = config.provider_configs["openai"]
    assert openai_config.base_url == "https://api.openai.example/v1"
    assert openai_config.api_key_env_var == "MY_OPENAI_KEY"
    assert openai_config.timeout_seconds == 4.5
    assert openai_config.retry_count == 2
    assert openai_config.options == {"model": "gpt-test"}
    assert "secret" not in repr(config)


def test_settings_service_updates_history_preferences() -> None:
    store = InMemoryConfigStore()
    service = SettingsService(store)

    config = service.update_history_preferences(enabled=True, max_entries="25")

    assert config.history_enabled is True
    assert config.history_max_entries == 25


def test_settings_service_ignores_invalid_history_max_entries() -> None:
    store = InMemoryConfigStore(AppConfig(history_max_entries=10))
    service = SettingsService(store)

    config = service.update_history_preferences(max_entries="-1")

    assert config.history_max_entries == 10


def test_settings_service_updates_ui_preferences() -> None:
    store = InMemoryConfigStore(AppConfig(ui_preferences={"density": "compact"}))
    service = SettingsService(store)

    config = service.update_ui_preferences({"theme": "light"})

    assert config.ui_preferences == {"density": "compact", "theme": "light"}


def test_settings_service_can_add_new_provider_config() -> None:
    store = InMemoryConfigStore(AppConfig(provider_configs={}))
    service = SettingsService(store)

    config = service.update_provider_runtime_config(
        "custom",
        base_url="https://custom.example",
    )

    assert isinstance(config.provider_configs["custom"], ProviderRuntimeConfig)
    assert config.provider_configs["custom"].base_url == "https://custom.example"
