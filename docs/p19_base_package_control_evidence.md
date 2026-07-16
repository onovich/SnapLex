# P19 Base Package Control Evidence

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: PASS

P19 revalidates the deterministic `base` package lane as the control path. The
base lane must remain keyring-free, fake-smoke capable, and fail-closed for real
provider launch when real provider setup is missing.

## Base Package Build

Command:

```powershell
python scripts\package_windows.py --variant base
```

Result: PASS. PyInstaller completed and reported
`SNAPLEX_PACKAGE_VARIANT=base`.

## Packaged Workflow Smoke

Command:

```powershell
cmd /c SmokeTrial.cmd
```

Result: PASS.

Evidence:

- source `SnapLex 0.1.0` check passed;
- source no-GUI bootstrap passed;
- package dry-run reported `SNAPLEX_PACKAGE_VARIANT=base`;
- packaged workflow smoke passed with fake provider;
- clipboard translation smoke passed;
- screen fake capture/OCR translation smoke passed;
- history record/list/delete/clear smoke passed.

## Packaged Fake Trial

Command:

```powershell
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS. Packaged fake smoke mode launched without real translation.

## Packaged Real Trial Expected Rejection

Command:

```powershell
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: PASS as expected rejection. The command exited nonzero and reported
that real translation provider setup is not configured.

## Base Credential Smoke Expected Rejection

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection. Output reported:
`keyring is not available in this runtime`.

This confirms the base package did not silently include keyring support.

## Local Output Boundary

Package outputs were generated only under ignored local paths such as `build/`
and `dist/`. They are not staged and must not be committed.

## Round 3 Self-Checks

Debug self-check:

- The evidence is explained by the smallest base control workflow: build base,
  smoke fake package, confirm real-provider fail-closed behavior, and confirm
  credential smoke rejects keyring.
- Success, expected rejection, keyring absence, ignored local output, and
  no-secret states are covered.

Architecture self-check:

- Base package validation did not change provider, credential, settings,
  history, capture, OCR, UI, package specification, or trial readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
