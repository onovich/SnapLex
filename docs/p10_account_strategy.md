# P10 Credential And Account Strategy

Date: 2026-07-15
Phase: P10 Secure Credential And Account Strategy
Status: implemented local strategy, future account strategy documented

P10 gives SnapLex a secure local credential boundary without adding production
accounts, SnapLex Cloud, billing, OAuth, or a hosted token broker. The accepted
runtime paths are environment variables and optional local OS keyring storage.
Both paths keep raw provider secrets out of config, history, docs, tests, logs,
screenshots, package resources, and git.

## Accepted Local Credential Paths

Environment variables remain the compatibility path for existing users,
scripts, CI-like smoke runs, and short-lived shell sessions. SnapLex stores only
the environment variable name, such as `SNAPLEX_OPENAI_API_KEY`, and resolves
the value at provider call time through `CredentialService`.

Local secure credential storage is available through the optional
`credentials` extra:

```powershell
python -m pip install -e ".[gui,credentials]"
```

When a provider uses `credential_source=keyring`, SnapLex stores only a
non-secret credential identifier such as `snaplex/openai/default` in config.
The provider secret is saved and deleted through the OS keyring via the lazy
`KeyringCredentialStore`. Automated tests use fake or mocked stores and never
require a real OS keyring.

Use this source setup for a local OpenAI keyring trial:

```powershell
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai"
$env:SNAPLEX_OPENAI_CREDENTIAL_SOURCE = "keyring"
$env:SNAPLEX_OPENAI_CREDENTIAL_IDENTIFIER = "snaplex/openai/default"
python -m snaplex
```

Open `Settings`, choose `Local secure credential`, paste the provider key into
the transient password field, and save it. SnapLex clears the field after the
operation and never writes the value to config.

## Readiness Checks

Use the no-network readiness check before real trial launch:

```powershell
python -m snaplex --check-real-provider
```

The command succeeds only when a non-fake provider has an accepted credential or
endpoint source. It prints credential source/status text, not secret values.

`StartTrial.cmd` and `StartPackagedTrial.cmd` call the same readiness boundary.
They must reject missing real provider setup instead of silently falling back to
fake translation. `StartFakeTrial.cmd`, `StartPackagedFakeTrial.cmd`, and
`SmokeTrial.cmd` remain deterministic fake smoke paths.

## Tradeoffs

Environment variables are simple, scriptable, and transparent. They are still
visible to the current process environment, so users should set them only in
local shells or ignored launchers and rotate provider keys as needed.

OS keyring storage improves local desktop ergonomics because the secret value
does not live in SnapLex config. It depends on the user's OS keyring backend and
the optional `keyring` dependency, so unsupported or locked backends must show a
clear unavailable state without breaking app launch, no-GUI bootstrap, package
dry-run, or automated tests.

SnapLex Cloud or a hosted token broker could hide provider secrets from the
desktop and support short-lived tokens, revocation, billing, and policy
controls. That path requires backend ownership, threat modeling, account
security, provider contract review, operations, and privacy policy work. It is
explicitly outside P10.

Provider account OAuth or enterprise identity could be useful where providers
support delegated identity. It still requires account UX, token refresh,
revocation, secure storage, and provider-specific compliance review. It is not
enabled in P10; `Connect account (future)` stays disabled.

Self-hosted LibreTranslate is the simplest no-secret real-provider option when
the local endpoint does not require an API key. If the endpoint requires a key,
it uses the same environment or keyring credential boundary as other providers.

## P11 Candidates

Recommended next work is trial hardening around real-provider onboarding:

- manual Windows Credential Locker smoke with a throwaway provider key;
- explicit packaged credential variant decision if keyring support should ship
  in a distributable binary;
- clearer first-run setup copy if trial users struggle with provider accounts;
- provider-specific least-privilege and key-rotation notes.

Production SnapLex Cloud, account OAuth, billing, and a hosted token broker
remain future architecture work requiring explicit approval.
