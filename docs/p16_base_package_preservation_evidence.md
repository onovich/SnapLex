# P16 Base Package Preservation Evidence

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: base package preservation PASS

P16 Round 2 proves that the deterministic base package remains the default
private-trial smoke path and does not silently include keyring support. The
credential-capable path remains explicit as the `credentials` package variant.

## Base Build Evidence

Command:

```cmd
python scripts\package_windows.py --variant base
```

Result: PASS.

Observed output included:

```text
SNAPLEX_PACKAGE_VARIANT=base
Build complete! The results are available in: D:\ToolProjects\SnapLex\dist
```

The generated `build\` and `dist\` outputs are local ignored artifacts and are
not committed.

## Base Fake Package Smoke

Command:

```cmd
cmd /c SmokeTrial.cmd
```

Result: PASS.

Observed packaged workflow evidence:

```text
SnapLex packaged workflow smoke PASS
- settings persistence: fake provider, history enabled
- clipboard translation: hello -> hello [en]
- screen fake capture/OCR translation: screen hello -> screen hello [en]
- history record/list/delete/clear: PASS
```

Command:

```cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS.

Observed output kept the fake-mode label visible:

```text
Provider: fake smoke mode; this is not real translation.
SnapLex bootstrap OK (PySide6 available).
```

## Base Real-Trial Fail-Closed Behavior

Command:

```cmd
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: expected rejection PASS.

Observed output:

```text
Real translation provider is not configured.
```

The command continues to direct maintainers to real-provider setup for real
translation and to fake commands for package smoke.

## Base Credential Smoke Rejection

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: expected rejection PASS.

Observed output:

```text
SnapLex packaged credential smoke FAIL: keyring is not available in this runtime.
```

This is the intended base package behavior. It proves keyring was not silently
included in the base package and that credential-capable smoke remains limited
to the explicit `credentials` variant.

## Artifact Boundary Check

Command:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models
```

Result: PASS, no tracked generated artifacts.

## Round 11 Base Restore Rehearsal

After rerunning the credential candidate gate in Round 11, P16 rebuilt the base
package to return local `dist\SnapLex` to the deterministic default lane.

Commands:

```cmd
python scripts\package_windows.py --variant base
cmd /c SmokeTrial.cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
cmd /c StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS.

Observed outcomes:

- base build printed `SNAPLEX_PACKAGE_VARIANT=base`;
- packaged workflow smoke passed;
- packaged fake trial no-gui passed;
- packaged real trial rejected missing real-provider setup;
- base credential smoke rejected keyring with
  `keyring is not available in this runtime`;
- generated package and smoke folders remained ignored and untracked.

## Round 2 Self-Checks

Debug self-check:

- The current evidence is explained by the smallest base package workflow:
  build, fake smoke, real-trial expected rejection, and credential-smoke
  expected rejection.
- Success, expected rejection, generated-output hygiene, and no-secret states
  are covered.
- Credential variant build and credential smoke hardening are deferred to later
  P16 rounds.

Architecture self-check:

- Base package behavior remains deterministic and keyring-free.
- Credential-capable package behavior remains opt-in through the explicit
  `credentials` variant.
- Provider, credential, settings, history, OCR, capture, and UI business rules
  remain outside packaging scripts.
