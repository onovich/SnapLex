# P10 Credential Strategy Decisions

Date: 2026-07-15
Phase: P10 Secure Credential And Account Strategy
Status: Round 1 decision record

P10 starts from the planner-accepted P9 baseline at
`a2ebc99a47bc810fe3f6245f61a26a16fc6650b3`. SnapLex is visually trial-ready,
but real-provider users still need local environment variables. P10 introduces
a credential boundary and a local secure-storage path without adding production
cloud, account OAuth, billing, or a hosted token broker.

## Baseline Revalidation

Round 1 revalidated the P9 baseline before credential work:

- `Validate.cmd`: PASS with 221 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.

No real provider credentials, OS keyring, network calls, package artifacts, or
screenshots were required for this baseline.

## Authentication Reality

Official provider and platform documentation confirms the P10 direction:

- OpenAI API requests use bearer credentials from API keys or short-lived
  workload identity tokens. API keys are secrets and should be loaded from an
  environment variable or a server-side key management system:
  `https://developers.openai.com/api/reference/overview#authentication`.
- DeepL API access requires an authentication key, says keys must remain
  confidential, and says not to use API keys in client-side code:
  `https://developers.deepl.com/docs/getting-started/auth`.
- Azure Translator supports subscription keys, bearer tokens, and Microsoft
  Entra ID, but each path still requires an Azure resource/account boundary:
  `https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/authentication`.
- Windows Credential Locker is the Windows-native credential storage direction
  for desktop apps:
  `https://learn.microsoft.com/en-us/windows/apps/develop/security/credential-locker`.
- Python `keyring` provides a cross-platform wrapper for system keyrings,
  including Windows Credential Locker, macOS Keychain, and Linux Secret
  Service/KWallet:
  `https://pypi.org/project/keyring/`.

## Threat Model

P10 protects against accidental leakage through project-controlled surfaces:

- raw secrets serialized into `config.json` or future config migrations;
- raw secrets written to translation history;
- raw secrets rendered in Settings labels, accessibility metadata, tooltips,
  screenshots, status text, or connection-test results;
- raw secrets embedded in provider errors, reprs, logs, docs, tests, or sample
  fixtures;
- raw secrets copied into `.env`, package resources, generated package outputs,
  local smoke data, screenshot folders, or git;
- raw secrets added accidentally by broad `git add`;
- optional keyring imports breaking no-GUI bootstrap, tests, package dry-run, or
  environments without a keyring backend.

P10 does not attempt to protect against a fully compromised local OS account,
debugger, memory scraper, malicious local process, or provider-side account
compromise. Those risks require OS security, endpoint protection, account
rotation, least-privilege provider keys, and future backend/account design.

## Decision

P10 will implement two accepted credential sources:

1. Environment variables remain first-class and backward compatible.
2. Optional local OS keyring storage is added behind a lazy credential
   service/store boundary and fake/mocked automated tests.

Config may store provider names, endpoints, model/options, timeout/retry,
environment variable names, and credential references. Config must not store
raw secret values.

`fake` remains deterministic smoke/dev mode and is not treated as a real
credential path.

## Credential Boundary Shape

P10 will introduce service/store concepts such as:

- `CredentialReference`: source type plus non-secret lookup id.
- `CredentialStatus`: ready, missing, unsupported, unavailable, saved, deleted,
  or failed without secret values.
- `CredentialService`: resolve, save, delete, and status operations.
- `EnvironmentCredentialStore`: resolves existing env var names.
- `InMemoryCredentialStore`: deterministic fake store for tests.
- `KeyringCredentialStore`: optional lazy wrapper around Python `keyring`.

Provider setup, provider registry, Test Connection, trial readiness, and
Settings must use this boundary. PySide6 widgets may collect a transient secret
for save/test, but widgets must not own provider or credential rules.

## Compatibility

Existing P8/P9 users continue to work with:

- `SNAPLEX_OPENAI_API_KEY`
- `SNAPLEX_DEEPL_API_KEY`
- `SNAPLEX_LIBRETRANSLATE_API_KEY`
- standard fallback names such as `OPENAI_API_KEY` and `DEEPL_API_KEY` where
  trial scripts already detect them.

Existing configs with only `api_key_env_var` migrate to an environment
credential reference. LibreTranslate stays endpoint-only unless an API-key env
var name or secure credential reference is configured.

## Account And Cloud Decision

P10 does not enable `Connect account (future)`. Account sign-in remains disabled
because production OAuth, consumer account linking, billing, cloud sync, and a
hosted token broker need explicit backend/security approval.

P10 will document future options in `docs/p10_account_strategy.md`, including
environment variables, OS keyring, SnapLex Cloud token broker, provider OAuth or
enterprise identity, and self-hosted LibreTranslate.

## Round 1 Debug Self-Check

- The change is explainable as credential strategy and threat-model setup.
- Failure surfaces are docs, source-reality drift, and baseline validation.
- Success, missing credential, unsupported store, keyring unavailability,
  fake mode, and no-GUI states are represented as strategy requirements for
  later rounds.
- No raw secret entered docs, tests, logs, screenshots, config, or package
  resources.

## Round 1 Architecture Self-Check

- Credential state will live behind service/store boundaries.
- UI will render credential status and transient input only.
- Provider adapters will receive resolved credentials through provider config
  or resolver boundaries.
- Production cloud/OAuth/billing remains out of runtime scope.
- Generated outputs and local smoke artifacts remain ignored and uncommitted.
