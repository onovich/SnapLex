from snaplex.storage import AppConfig, InMemoryConfigStore, load_app_config_from_environment


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
