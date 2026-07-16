# P22 Base Package Continuity Evidence

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: deterministic base package lane revalidated

P22 revalidated the deterministic `base` package lane after refreshing
unsigned/private-trial support documentation. The base lane remains
keyring-free and fake-smoke deterministic.

## Commands And Results

### Base Package Build

Command:

```cmd
python scripts\package_windows.py --variant base
```

Result: PASS.

Evidence:

- PyInstaller completed successfully.
- Output was written under local ignored `dist\SnapLex`.
- Build output reported `SNAPLEX_PACKAGE_VARIANT=base`.

### Base Package Dry-Run

Command:

```cmd
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS.

Evidence:

- Dry-run printed the expected PyInstaller command.
- Dry-run reported `SNAPLEX_PACKAGE_VARIANT=base`.

### Source Real Trial Missing-Provider Guard

Command:

```cmd
cmd /c StartTrial.cmd --no-gui
```

Result: PASS as expected rejection.

Evidence:

- Process exited with code `1`.
- Output reported `Real translation provider is not configured.`
- Output recommended fake trial commands for smoke use.
- No fallback to fake as real translation occurred.

### Source Fake Trial

Command:

```cmd
cmd /c StartFakeTrial.cmd --no-gui
```

Result: PASS.

Evidence:

- Output reported `Provider: fake smoke mode; this is not real translation.`
- Output reported `SnapLex bootstrap OK (PySide6 available).`

### Trial Smoke

Command:

```cmd
cmd /c SmokeTrial.cmd
```

Result: PASS.

Evidence:

- Output reported `SnapLex 0.1.0`.
- Output reported `SNAPLEX_PACKAGE_VARIANT=base`.
- Packaged executable smoke passed.
- Clipboard, fake screen capture/OCR translation, settings persistence, and
  history record/list/delete/clear smoke paths passed.

### Packaged Fake Trial

Command:

```cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS.

Evidence:

- Output reported `Starting packaged SnapLex in fake smoke mode`.
- Output reported `Provider: fake smoke mode; this is not real translation.`
- Output reported `SnapLex bootstrap OK (PySide6 available).`

### Packaged Real Trial Missing-Provider Guard

Command:

```cmd
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: PASS as expected rejection.

Evidence:

- Process exited with code `1`.
- Output reported `Real translation provider is not configured.`
- No fallback to fake as real translation occurred.

### Base Credential Smoke Control

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection.

Evidence:

- Process exited with code `1`.
- Output reported `SnapLex packaged credential smoke FAIL: keyring is not
  available in this runtime.`
- This confirms the base package remains keyring-free.

## Ignored Local Artifact State

Command:

```cmd
git status --short --ignored
```

Result: PASS.

Observed ignored entries:

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

No nonignored package output, screenshot, log, local app data, smoke data, OCR
cache, `.env`, keyring export, tester personal data, certificate, private key,
signed binary, timestamp response, signing material, or provider secret was
present after base lane validation.

## Decision

Base package continuity: PASS.

The deterministic base package lane remains suitable for unsigned private-trial
fake smoke. It remains separate from the explicit credentials package lane and
does not include keyring support.

## Round 5 Self-Checks

Debug self-check:

- Success, expected rejection, generated artifact, ignored output, no-keyring,
  no-fallback, and no-secret states are covered.
- Source fake, packaged fake, source real rejection, packaged real rejection,
  base package build, dry-run, smoke, and base credential control were checked.

Architecture self-check:

- The validation does not move credential behavior into UI or package scripts.
- The base package remains deterministic and keyring-free.
- Providers remain behind the provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
