# P11 Provider Onboarding Notes

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: onboarding guidance updated

P11 keeps provider onboarding local and explicit. SnapLex does not include
production account sign-in, SnapLex Cloud, billing, OAuth, or a token broker.
Private trial users choose one of three paths.

## Path 1: Fake Smoke Mode

Use fake mode to validate launch, UI, packaging, settings, history, and smoke
commands without network or credentials:

```cmd
StartFakeTrial.cmd
StartPackagedFakeTrial.cmd
SmokeTrial.cmd
```

Fake output is deterministic placeholder text such as `hello [zh]`. It is
always labeled as fake smoke mode and is not real translation.

## Path 2: Environment Variables

Use environment variables when testing real providers from source or packaged
trials:

```powershell
$env:SNAPLEX_OPENAI_API_KEY = "<local provider key>"
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai"
StartTrial.cmd
```

SnapLex stores the variable name, not the value. Keep provider keys in the
current shell, an ignored local launcher, or another local secret manager. Do
not paste provider keys into Settings env-var fields, docs, issues,
screenshots, logs, commits, or chat.

## Path 3: Local Secure Credential From Source

Use the optional credentials extra only when the local environment can install
and use `keyring`:

```powershell
python -m pip install -e ".[gui,credentials]"
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai"
$env:SNAPLEX_OPENAI_CREDENTIAL_SOURCE = "keyring"
$env:SNAPLEX_OPENAI_CREDENTIAL_IDENTIFIER = "snaplex/openai/default"
python -m snaplex
```

In Settings, choose `Local secure credential`, paste the provider key into the
password-style local secret field, and save it. SnapLex stores only the keyring
identifier in config. The base package does not promise keyring support in P11.

## Readiness And Test Connection

Use the no-network readiness check before launching real trial commands:

```powershell
python -m snaplex --check-real-provider
```

Use `Test Connection` only when you intentionally want SnapLex to contact the
selected provider. Automated tests and release smoke use mocked or fake paths.

## Key Rotation And Least Privilege

Use a separate short-lived trial key with low quota or budget controls whenever
the provider account supports them. Keep raw keys only in the active shell, an
ignored local launcher, or the optional local OS keyring. Rotate keys before
handing a build to another tester and after any suspected exposure.

See `docs/p11_key_rotation_least_privilege.md` for the full private-trial
checklist.

## Missing Provider Behavior

Real trial commands must fail closed when no real provider credential or
accepted endpoint exists:

```cmd
StartTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

```text
Real translation provider is not configured.
```

Use fake trial commands when the goal is packaging or UI smoke without real
translation.

## Future Account Sign-In

The `Connect account (future)` affordance remains disabled. Enabling it requires
a later backend/security decision covering account identity, token handling,
provider contracts, billing, privacy policy, and revocation.

## P12 Private Pilot Feedback

For the first controlled private pilot, use
`docs/p12_private_trial_release_notes.md` for tester-facing instructions,
`docs/p12_feedback_intake_template.md` for sanitized reports, and
`docs/p12_trial_triage_workflow.md` for maintainer triage. Real-provider smoke
remains optional/manual; see `docs/p12_real_provider_smoke_decision.md`.
