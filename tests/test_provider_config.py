import pytest

from snaplex.errors import MissingProviderCredentialError
from snaplex.providers.config import (
    ProviderRuntimeConfig,
    copy_provider_runtime_configs,
    default_provider_runtime_configs,
    provider_credential_reference,
    resolve_api_key,
)
from snaplex.services.credentials import (
    EnvironmentCredentialStore,
    CredentialService,
    CredentialSource,
)


def test_default_provider_runtime_configs_do_not_store_secrets() -> None:
    configs = default_provider_runtime_configs()

    assert configs["fake"].api_key_env_var == ""
    assert configs["libretranslate"].base_url == "http://localhost:5000"
    assert configs["openai"].api_key_env_var == "SNAPLEX_OPENAI_API_KEY"
    assert configs["openai"].options["model"] == "gpt-5.5"
    assert configs["deepl"].api_key_env_var == "SNAPLEX_DEEPL_API_KEY"


def test_provider_runtime_config_trims_base_url() -> None:
    config = ProviderRuntimeConfig(base_url="https://example.test///")

    assert config.base_url_without_trailing_slash() == "https://example.test"


def test_copy_provider_runtime_configs_copies_options() -> None:
    configs = {"openai": ProviderRuntimeConfig(options={"model": "a"})}

    copied = copy_provider_runtime_configs(configs)
    copied["openai"].options["model"] = "b"

    assert configs["openai"].options == {"model": "a"}


def test_resolve_api_key_uses_supplied_environment_mapping() -> None:
    config = ProviderRuntimeConfig(api_key_env_var="SNAPLEX_EXAMPLE_API_KEY")

    assert (
        resolve_api_key(
            "example",
            config,
            environ={"SNAPLEX_EXAMPLE_API_KEY": " secret "},
        )
        == "secret"
    )


def test_resolve_api_key_uses_credential_service_boundary() -> None:
    config = ProviderRuntimeConfig(api_key_env_var="SNAPLEX_EXAMPLE_API_KEY")
    credential_service = CredentialService(
        {
            CredentialSource.ENVIRONMENT: EnvironmentCredentialStore(
                {"SNAPLEX_EXAMPLE_API_KEY": " service-secret "},
            ),
        },
    )

    assert (
        resolve_api_key(
            "example",
            config,
            environ={},
            credential_service=credential_service,
        )
        == "service-secret"
    )


def test_resolve_api_key_raises_when_env_var_name_is_missing() -> None:
    config = ProviderRuntimeConfig()

    with pytest.raises(MissingProviderCredentialError) as exc_info:
        resolve_api_key("example", config, environ={})

    assert exc_info.value.code == "missing_provider_credential"
    assert exc_info.value.provider_name == "example"
    assert exc_info.value.env_var == ""


def test_resolve_api_key_raises_when_env_value_is_missing() -> None:
    config = ProviderRuntimeConfig(api_key_env_var="SNAPLEX_EXAMPLE_API_KEY")

    with pytest.raises(MissingProviderCredentialError) as exc_info:
        resolve_api_key("example", config, environ={})

    assert exc_info.value.provider_name == "example"
    assert exc_info.value.env_var == "SNAPLEX_EXAMPLE_API_KEY"


def test_provider_credential_reference_defaults_to_environment_compatibility() -> None:
    reference = provider_credential_reference(
        "openai",
        ProviderRuntimeConfig(api_key_env_var="SNAPLEX_OPENAI_API_KEY"),
    )

    assert reference.provider_name == "openai"
    assert reference.source == CredentialSource.ENVIRONMENT
    assert reference.identifier == "SNAPLEX_OPENAI_API_KEY"


def test_provider_credential_reference_supports_keyring_without_secret_value() -> None:
    reference = provider_credential_reference(
        "openai",
        ProviderRuntimeConfig(credential_source="keyring"),
    )

    assert reference.source == CredentialSource.KEYRING
    assert reference.identifier == "snaplex/openai/default"
    assert "secret" not in repr(reference).lower()
