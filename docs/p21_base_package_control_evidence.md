# P21 Base Package Control Evidence

Date: 2026-07-17
Phase: P21 Signing Path Unblock Decision Or Pause Gate
Status: PASS

P21 revalidates the deterministic `base` package lane after recording signing
as PAUSED. The base package remains fake-smoke capable, real-provider
fail-closed, and keyring-free.

## Scope

This round validates the `base` package lane only.

It does not:

- build the `credentials` variant;
- run signing commands;
- create, import, purchase, invent, or use certificates;
- create signed artifacts;
- call timestamp services;
- commit package outputs.

## Commands And Results

Command:

```powershell
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS. Output reported `SNAPLEX_PACKAGE_VARIANT=base`.

Command:

```powershell
cmd /c StartTrial.cmd --no-gui
```

Result: PASS as expected rejection. The command exited with code 1 and missing
real provider setup was rejected.

Command:

```powershell
cmd /c StartFakeTrial.cmd --no-gui
```

Result: PASS. Fake smoke mode was clearly labeled as not real translation.

Command:

```powershell
cmd /c SmokeTrial.cmd
```

Result: PASS.

Evidence from output:

- version smoke: PASS, `SnapLex 0.1.0`;
- no-GUI bootstrap: PASS;
- base package dry-run/build path reported `SNAPLEX_PACKAGE_VARIANT=base`;
- packaged workflow smoke: PASS;
- settings persistence: PASS;
- clipboard fake translation: PASS;
- screen fake capture/OCR translation: PASS;
- history record/list/delete/clear: PASS.

Command:

```powershell
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS. Packaged fake smoke mode was clearly labeled as not real
translation.

Command:

```powershell
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: PASS as expected rejection. The command exited with code 1 and missing
real provider setup was rejected.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection. The command exited with code 1 and output
reported `keyring is not available in this runtime`.

## Ignored Artifact State

`git status --short --ignored` showed only ignored local outputs and caches:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- package `__pycache__/` directories
- `tests/__pycache__/`
- `tmp/`

No nonignored package output, signing material, certificate, private key,
signed binary, timestamp response, screenshot, log, `.env`, keyring export,
tester data, local app data, smoke data, OCR cache, or provider secret was
created.

## Decision

Decision: PASS.

The `base` package lane remains deterministic and keyring-free:

- base fake package smoke passes;
- real trial paths fail closed without real provider setup;
- credential smoke rejects keyring as unavailable;
- package outputs remain under ignored `build/`, `dist/`, and
  `snaplex-smoke-data/` paths;
- no generated package output, screenshot, log, certificate, private key,
  signed artifact, timestamp response, `.env`, keyring export, tester data,
  local app data, OCR cache, or provider secret is committed.

## Round 4 Self-Checks

Debug self-check:

- The evidence is explained by the smallest base-lane workflow: dry-run,
  source fake trial, package fake smoke, packaged real fail-closed, and base
  credential smoke expected rejection.
- Success, expected rejection, missing real provider, missing keyring in base,
  paused signing, no-signing-command, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- Base package validation does not change provider, credential, settings,
  history, capture, OCR, UI, package specification, or trial readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains separate and explicit.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
