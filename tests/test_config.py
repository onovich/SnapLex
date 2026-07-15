import json

from snaplex.providers.config import ProviderRuntimeConfig, resolve_api_key
from snaplex.storage import (
    APP_DATA_DIR_ENV_VAR,
    CONFIG_FILE_VERSION,
    AppConfig,
    InMemoryConfigStore,
    JsonFileConfigStore,
    app_config_from_dict,
    app_config_to_dict,
    default_app_data_dir,
    load_app_config_from_environment,
)


def test_config_defaults_use_fake_provider() -> None:
    config = AppConfig()

    assert config.source_lang == "auto"
    assert config.target_lang == "en"
    assert config.provider_name == "fake"
    assert config.provider_order == ("fake",)
    assert config.provider_configs["fake"].base_url == ""
    assert config.provider_configs["libretranslate"].base_url == "http://localhost:5000"
    assert config.provider_configs["openai"].api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
    assert config.provider_configs["openai"].options["model"] == "gpt-5.5"
    assert config.provider_configs["deepl"].api_key_env_var == "SNAPLEX_DEEPL_API_KEY"
    assert config.history_enabled is False
    assert config.history_max_entries == 50
    assert config.ui_preferences == {}


def test_in_memory_config_store_copies_nested_config() -> None:
    store = InMemoryConfigStore()
    config = AppConfig(provider_order=("fake", "backup"), ui_preferences={"theme": "compact"})

    store.save(config)
    loaded = store.load()
    loaded.provider_configs["openai"].options["model"] = "changed"
    loaded.ui_preferences["theme"] = "changed"

    assert store.load().ui_preferences == {"theme": "compact"}
    assert store.load().provider_configs["openai"].options["model"] == "gpt-5.5"
    assert store.load().provider_order == ("fake", "backup")


def test_load_app_config_from_environment_selects_provider_without_reading_secret() -> None:
    config = load_app_config_from_environment(
        {
            "SNAPLEX_PROVIDER": "openai",
            "SNAPLEX_PROVIDER_ORDER": "openai, fake",
            "SNAPLEX_SOURCE_LANG": "ja",
            "SNAPLEX_TARGET_LANG": "en",
            "SNAPLEX_OPENAI_BASE_URL": "https://api.openai.example/v1",
            "SNAPLEX_OPENAI_API_KEY_ENV": "MY_OPENAI_KEY",
            "SNAPLEX_OPENAI_API_KEY": "secret-value",
            "SNAPLEX_OPENAI_TIMEOUT_SECONDS": "3.5",
            "SNAPLEX_OPENAI_RETRY_COUNT": "2",
            "SNAPLEX_OPENAI_MODEL": "gpt-test",
        },
    )

    openai_config = config.provider_configs["openai"]
    assert config.provider_name == "openai"
    assert config.provider_order == ("openai", "fake")
    assert config.source_lang == "ja"
    assert config.target_lang == "en"
    assert openai_config.base_url == "https://api.openai.example/v1"
    assert openai_config.api_key_env_var == "MY_OPENAI_KEY"
    assert openai_config.timeout_seconds == 3.5
    assert openai_config.retry_count == 2
    assert openai_config.options["model"] == "gpt-test"
    assert "secret-value" not in repr(config)


def test_load_app_config_from_environment_ignores_invalid_numeric_values() -> None:
    config = load_app_config_from_environment(
        {
            "SNAPLEX_PROVIDER": "deepl",
            "SNAPLEX_DEEPL_TIMEOUT_SECONDS": "-1",
            "SNAPLEX_DEEPL_RETRY_COUNT": "not-an-int",
            "SNAPLEX_DEEPL_MODEL_TYPE": "quality_optimized",
        },
    )

    deepl_config = config.provider_configs["deepl"]
    assert deepl_config.timeout_seconds == 20.0
    assert deepl_config.retry_count == 0
    assert deepl_config.options["model_type"] == "quality_optimized"


def test_default_app_data_dir_uses_explicit_override(tmp_path) -> None:
    config_dir = tmp_path / "snaplex-data"

    assert default_app_data_dir({APP_DATA_DIR_ENV_VAR: str(config_dir)}) == config_dir


def test_default_app_data_dir_uses_appdata_when_available(tmp_path) -> None:
    appdata = tmp_path / "AppData" / "Roaming"

    assert default_app_data_dir({"APPDATA": str(appdata)}) == appdata / "SnapLex"


def test_json_file_config_store_returns_defaults_for_missing_file(tmp_path) -> None:
    store = JsonFileConfigStore(tmp_path / "config.json")

    assert store.load() == AppConfig()


def test_json_file_config_store_saves_and_loads_config(tmp_path) -> None:
    store = JsonFileConfigStore(tmp_path / "config.json")
    config = AppConfig(
        source_lang="ja",
        target_lang="en",
        provider_name="openai",
        provider_order=("openai", "fake"),
        provider_configs={
            "openai": ProviderRuntimeConfig(
                base_url="https://api.openai.example/v1",
                api_key_env_var="MY_OPENAI_KEY",
                timeout_seconds=3.5,
                retry_count=2,
                options={"model": "gpt-test"},
            ),
        },
        history_enabled=True,
        history_max_entries=12,
        ui_preferences={"density": "compact"},
    )

    store.save(config)
    loaded = store.load()

    assert loaded.source_lang == "ja"
    assert loaded.target_lang == "en"
    assert loaded.provider_name == "openai"
    assert loaded.provider_order == ("openai", "fake")
    assert loaded.provider_configs["openai"].base_url == "https://api.openai.example/v1"
    assert loaded.provider_configs["openai"].api_key_env_var == "MY_OPENAI_KEY"
    assert loaded.provider_configs["openai"].timeout_seconds == 3.5
    assert loaded.provider_configs["openai"].retry_count == 2
    assert loaded.provider_configs["openai"].options == {"model": "gpt-test"}
    assert loaded.history_enabled is True
    assert loaded.history_max_entries == 12
    assert loaded.ui_preferences == {"density": "compact"}
    assert (tmp_path / "config.json.tmp").exists() is False


def test_json_file_config_store_returns_defaults_for_malformed_json(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{not-json", encoding="utf-8")
    store = JsonFileConfigStore(config_path)

    assert store.load() == AppConfig()


def test_json_file_config_store_migrates_legacy_payload(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "source_lang": "fr",
                "target_lang": "en",
                "provider_order": ["fake"],
                "history_enabled": True,
            },
        ),
        encoding="utf-8",
    )
    store = JsonFileConfigStore(config_path)

    loaded = store.load()

    assert loaded.source_lang == "fr"
    assert loaded.target_lang == "en"
    assert loaded.provider_order == ("fake",)
    assert loaded.provider_configs["openai"].api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
    assert loaded.provider_configs["deepl"].api_key_env_var == "SNAPLEX_DEEPL_API_KEY"
    assert loaded.history_enabled is True


def test_legacy_provider_api_key_env_var_remains_environment_compatible(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": CONFIG_FILE_VERSION,
                "provider_configs": {
                    "openai": {
                        "api_key_env_var": "LEGACY_OPENAI_KEY",
                    },
                },
            },
        ),
        encoding="utf-8",
    )
    store = JsonFileConfigStore(config_path)

    loaded = store.load()
    resolved = resolve_api_key(
        "openai",
        loaded.provider_configs["openai"],
        environ={"LEGACY_OPENAI_KEY": " legacy-secret "},
    )
    serialized_text = json.dumps(app_config_to_dict(loaded))

    assert loaded.provider_configs["openai"].api_key_env_var == "LEGACY_OPENAI_KEY"
    assert resolved == "legacy-secret"
    assert "legacy-secret" not in serialized_text


def test_app_config_serialization_does_not_keep_provider_secret_values() -> None:
    config = app_config_from_dict(
        {
            "version": CONFIG_FILE_VERSION,
            "provider_configs": {
                "openai": {
                    "base_url": "https://api.openai.example/v1",
                    "api_key_env_var": "SNAPLEX_OPENAI_API_KEY",
                    "api_key": "secret-value",
                    "api_key_value": "another-secret",
                    "timeout_seconds": 5,
                    "retry_count": 1,
                    "options": {"model": "gpt-test"},
                },
            },
        },
    )
    serialized = app_config_to_dict(config)
    serialized_text = json.dumps(serialized)

    assert config.provider_configs["openai"].api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
    assert "secret-value" not in repr(config)
    assert "secret-value" not in serialized_text
    assert "another-secret" not in serialized_text


def test_loaded_config_copies_mutable_fields(tmp_path) -> None:
    store = JsonFileConfigStore(tmp_path / "config.json")
    store.save(AppConfig(ui_preferences={"density": "compact"}))

    loaded = store.load()
    loaded.ui_preferences["density"] = "changed"
    loaded.provider_configs["openai"].options["model"] = "changed"

    reloaded = store.load()
    assert reloaded.ui_preferences == {"density": "compact"}
    assert reloaded.provider_configs["openai"].options["model"] == "gpt-5.5"
