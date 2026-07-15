from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.services.provider_setup import (
    ProviderSetupStatus,
    describe_provider_setup,
    describe_provider_setups,
)


def test_fake_provider_setup_is_labeled_as_smoke_mode() -> None:
    state = describe_provider_setup("fake")

    assert state.status == ProviderSetupStatus.FAKE_SMOKE
    assert state.is_fake is True
    assert state.is_real_provider is False
    assert state.can_test_connection is False
    assert "not real translation" in state.detail_text


def test_openai_provider_setup_reports_missing_credential_by_env_var_name() -> None:
    state = describe_provider_setup(
        "openai",
        ProviderRuntimeConfig(api_key_env_var="SNAPLEX_OPENAI_API_KEY"),
        environ={},
    )

    assert state.status == ProviderSetupStatus.MISSING_CREDENTIAL
    assert state.api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
    assert state.api_key_present is False
    assert state.can_test_connection is False
    assert "SNAPLEX_OPENAI_API_KEY" in state.detail_text


def test_openai_provider_setup_reports_ready_without_exposing_secret_value() -> None:
    state = describe_provider_setup(
        "openai",
        ProviderRuntimeConfig(api_key_env_var="SNAPLEX_OPENAI_API_KEY"),
        environ={"SNAPLEX_OPENAI_API_KEY": "test-secret-value"},
    )

    assert state.status == ProviderSetupStatus.READY_FROM_ENVIRONMENT
    assert state.api_key_present is True
    assert state.can_test_connection is True
    assert "test-secret-value" not in repr(state)
    assert "key value is not stored" in state.detail_text


def test_deepl_provider_setup_requires_env_credential() -> None:
    state = describe_provider_setup(
        "deepl",
        ProviderRuntimeConfig(api_key_env_var="SNAPLEX_DEEPL_API_KEY"),
        environ={},
    )

    assert state.status == ProviderSetupStatus.MISSING_CREDENTIAL
    assert state.display_name == "DeepL"


def test_libretranslate_provider_setup_can_be_ready_with_endpoint_only() -> None:
    state = describe_provider_setup(
        "libretranslate",
        ProviderRuntimeConfig(base_url="http://localhost:5000"),
        environ={},
    )

    assert state.status == ProviderSetupStatus.READY_FROM_ENVIRONMENT
    assert state.base_url == "http://localhost:5000"
    assert state.api_key_env_var == ""
    assert state.can_test_connection is True


def test_libretranslate_provider_setup_honors_configured_required_key_env() -> None:
    state = describe_provider_setup(
        "libretranslate",
        ProviderRuntimeConfig(
            base_url="http://localhost:5000",
            api_key_env_var="SNAPLEX_LIBRETRANSLATE_API_KEY",
        ),
        environ={},
    )

    assert state.status == ProviderSetupStatus.MISSING_CREDENTIAL
    assert state.can_test_connection is False


def test_provider_setup_rejects_unknown_provider() -> None:
    state = describe_provider_setup("custom")

    assert state.status == ProviderSetupStatus.UNSUPPORTED_PROVIDER
    assert state.can_test_connection is False


def test_provider_setup_collection_uses_supported_display_order() -> None:
    states = describe_provider_setups(
        {
            "openai": ProviderRuntimeConfig(api_key_env_var="OPENAI_API_KEY"),
        },
        environ={"OPENAI_API_KEY": "secret"},
    )

    assert tuple(state.provider_name for state in states) == (
        "fake",
        "libretranslate",
        "openai",
        "deepl",
    )
    assert states[2].status == ProviderSetupStatus.READY_FROM_ENVIRONMENT
