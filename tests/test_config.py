from snaplex.storage import AppConfig, InMemoryConfigStore


def test_config_defaults_use_fake_provider() -> None:
    config = AppConfig()

    assert config.source_lang == "auto"
    assert config.target_lang == "en"
    assert config.provider_name == "fake"
    assert config.provider_order == ("fake",)
    assert config.provider_configs["fake"].base_url == ""
    assert config.provider_configs["libretranslate"].base_url == "http://localhost:5000"
    assert config.provider_configs["openai"].api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
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
    assert store.load().provider_configs["openai"].options["model"] == "gpt-4o-mini"
    assert store.load().provider_order == ("fake", "backup")
