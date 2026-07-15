"""No-network readiness checks for real-provider trial launchers."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from snaplex.credentials import CredentialService
from snaplex.providers.config import ProviderRuntimeConfig, default_provider_runtime_configs
from snaplex.services.provider_setup import ProviderSetupState, describe_provider_setup
from snaplex.storage import AppConfig, JsonFileConfigStore, load_app_config_from_environment


@dataclass(frozen=True)
class TrialReadinessResult:
    ready: bool
    provider_name: str
    status_text: str
    detail_lines: tuple[str, ...] = ()


def check_real_provider_readiness(
    *,
    environ: Mapping[str, str] | None = None,
    config: AppConfig | None = None,
    credential_service: CredentialService | None = None,
) -> TrialReadinessResult:
    env = os.environ if environ is None else environ
    runtime_config = config or _load_trial_config(env)
    candidates = _candidate_provider_names(runtime_config, env)
    states = tuple(
        describe_provider_setup(
            provider_name,
            runtime_config.provider_configs.get(provider_name),
            environ=env,
            credential_service=credential_service,
        )
        for provider_name in candidates
    )
    ready_state = next((state for state in states if state.can_test_connection), None)
    if ready_state is not None:
        return TrialReadinessResult(
            ready=True,
            provider_name=ready_state.provider_name,
            status_text=f"Real provider ready: {ready_state.display_name}",
            detail_lines=(_state_line(ready_state),),
        )

    detail_lines = tuple(_state_line(state) for state in states)
    return TrialReadinessResult(
        ready=False,
        provider_name="",
        status_text="Real translation provider is not configured.",
        detail_lines=detail_lines,
    )


def _load_trial_config(env: Mapping[str, str]) -> AppConfig:
    return JsonFileConfigStore(
        default_config=load_app_config_from_environment(env),
    ).load()


def _candidate_provider_names(
    config: AppConfig,
    env: Mapping[str, str],
) -> tuple[str, ...]:
    provider_configs = {**default_provider_runtime_configs(), **config.provider_configs}
    candidates: list[str] = []
    for provider_name in (config.provider_name, *config.provider_order):
        _append_real_provider(candidates, provider_name)

    if _env_has_openai(env) or _has_explicit_credential(provider_configs["openai"]):
        _append_real_provider(candidates, "openai")
    if _env_has_deepl(env) or _has_explicit_credential(provider_configs["deepl"]):
        _append_real_provider(candidates, "deepl")
    if _env_has_libretranslate(env) or _has_explicit_credential(provider_configs["libretranslate"]):
        _append_real_provider(candidates, "libretranslate")
    return tuple(candidates)


def _append_real_provider(candidates: list[str], provider_name: str) -> None:
    normalized = provider_name.strip().lower()
    if normalized and normalized != "fake" and normalized not in candidates:
        candidates.append(normalized)


def _has_explicit_credential(config: ProviderRuntimeConfig) -> bool:
    return bool(config.credential_source.strip())


def _env_has_openai(env: Mapping[str, str]) -> bool:
    return bool(
        env.get("SNAPLEX_OPENAI_API_KEY", "").strip()
        or (
            env.get("OPENAI_API_KEY", "").strip()
            and env.get("SNAPLEX_OPENAI_API_KEY_ENV", "").strip() == "OPENAI_API_KEY"
        )
        or env.get("SNAPLEX_OPENAI_CREDENTIAL_SOURCE", "").strip()
    )


def _env_has_deepl(env: Mapping[str, str]) -> bool:
    return bool(
        env.get("SNAPLEX_DEEPL_API_KEY", "").strip()
        or (
            env.get("DEEPL_API_KEY", "").strip()
            and env.get("SNAPLEX_DEEPL_API_KEY_ENV", "").strip() == "DEEPL_API_KEY"
        )
        or env.get("SNAPLEX_DEEPL_CREDENTIAL_SOURCE", "").strip()
    )


def _env_has_libretranslate(env: Mapping[str, str]) -> bool:
    return bool(
        env.get("SNAPLEX_LIBRETRANSLATE_BASE_URL", "").strip()
        or env.get("SNAPLEX_LIBRETRANSLATE_CREDENTIAL_SOURCE", "").strip()
    )


def _state_line(state: ProviderSetupState) -> str:
    detail = state.detail_text.strip()
    if detail:
        return f"{state.display_name}: {state.status_text} - {detail}"
    return f"{state.display_name}: {state.status_text}"
