# P18 Package Validation Evidence

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: PASS

P18 package validation preserves the deterministic `base` package lane and the
explicit `credentials` package lane. Package outputs were generated only in
ignored local paths and were not staged.

## Base Package Lane

Command:

```powershell
python scripts\package_windows.py --variant base
```

Result: PASS. PyInstaller completed and reported
`SNAPLEX_PACKAGE_VARIANT=base`.

Command:

```powershell
cmd /c SmokeTrial.cmd
```

Result: PASS. Source version/no-GUI checks passed, package dry-run reported
the base variant, and packaged workflow smoke passed with fake provider,
clipboard translation, screen fake capture/OCR translation, and history
record/list/delete/clear.

Command:

```powershell
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS. Packaged fake smoke mode bootstrapped without real translation.

Command:

```powershell
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: PASS as expected rejection. The command exited nonzero and reported
that real translation provider setup is not configured.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection for the base package. Output reported:
`keyring is not available in this runtime`.

## Credentials Package Lane

Command:

```powershell
python scripts\package_windows.py --variant credentials
```

Result: PASS. PyInstaller completed, reported
`SNAPLEX_PACKAGE_VARIANT=credentials`, and analyzed
`keyring.backends.Windows`.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS. Output reported
`keyring.backends.Windows.WinVaultKeyring`, phase-neutral credential reference
`snaplex/package-credential-smoke`, and import/backend discovery PASS.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS. Output reported credential save/read/delete PASS and cleanup
PASS.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
```

Result: PASS. Output reported credential save PASS and retained a throwaway
credential for restart readiness.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS. Output reported credential restart readiness PASS and cleanup
PASS.

The smoke output did not print raw credential values.

## Final Base Restore

Command:

```powershell
python scripts\package_windows.py --variant base
```

Result: PASS. Local `dist\SnapLex` was restored to the base package variant.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection after final base restore. Output reported:
`keyring is not available in this runtime`.

## Local Output Boundary

Command:

```powershell
git status --short --ignored
```

Result: PASS. Only ignored local outputs and caches were present:

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

No package output, smoke app data, log, screenshot, certificate, private key,
keyring export, tester data, or provider secret was staged.

## Round 11 Self-Checks

Debug self-check:

- The evidence is explained by the smallest package workflow: build base,
  smoke base, verify base credential rejection, build credentials, smoke
  credential import/cycle/save/check-delete, then restore base.
- Success, expected rejection, cleanup, final base restore, and no-secret
  states are covered.

Architecture self-check:

- Package validation did not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness code.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
