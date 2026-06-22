from snaplex.storage import AppConfig, InMemoryConfigStore


def test_config_defaults_use_fake_provider() -> None:
    config = AppConfig()

    assert config.source_lang == "auto"
    assert config.target_lang == "en"
    assert config.provider_name == "fake"
    assert config.provider_order == ("fake",)
    assert config.ui_preferences == {}


def test_in_memory_config_store_copies_preferences() -> None:
    store = InMemoryConfigStore()
    config = AppConfig(provider_order=("fake", "backup"), ui_preferences={"theme": "compact"})

    store.save(config)
    loaded = store.load()
    loaded.ui_preferences["theme"] = "changed"

    assert store.load().ui_preferences == {"theme": "compact"}
    assert store.load().provider_order == ("fake", "backup")
