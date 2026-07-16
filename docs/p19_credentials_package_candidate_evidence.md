# P19 Credentials Package Candidate Evidence

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: PASS

P19 revalidates the explicit `credentials` package candidate lane. This lane
is private-trial only and remains separate from the deterministic `base`
package.

## Credentials Package Build

Command:

```powershell
python scripts\package_windows.py --variant credentials
```

Result: PASS.

Evidence:

- PyInstaller completed successfully.
- Output reported `SNAPLEX_PACKAGE_VARIANT=credentials`.
- PyInstaller analyzed `keyring.backends.Windows`.
- Package outputs were generated only under ignored local `build/` and `dist/`
  paths.

## Credential Import Smoke

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS.

Evidence:

- keyring backend:
  `keyring.backends.Windows.WinVaultKeyring`;
- credential reference:
  `snaplex/package-credential-smoke`;
- keyring import/backend discovery: PASS.

## Credential Cycle Smoke

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS.

Evidence:

- credential save/read/delete: PASS;
- credential cleanup: PASS.

## Credential Restart Readiness Smoke

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
```

Result: PASS. Credential save passed and a throwaway credential was retained
for restart readiness.

Command:

```powershell
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS. Credential restart readiness and cleanup both passed.

## Secret Hygiene

The credential smoke output reported only the backend, phase-neutral credential
reference, and PASS states. It did not print raw credential values.

No provider API keys, `.env` files, keyring exports, local app data,
screenshots, logs, package outputs, tester data, or provider secrets were
staged.

## Round 4 Self-Checks

Debug self-check:

- The evidence is explained by the smallest credentials candidate workflow:
  build explicit credentials variant, prove keyring backend discovery, run
  import/cycle/save/check-delete, and confirm cleanup.
- Success, cleanup, restart readiness, ignored local output, and no-secret
  states are covered.

Architecture self-check:

- Credentials package validation did not change provider, credential,
  settings, history, capture, OCR, UI, package specification, or trial
  readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
