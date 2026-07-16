# P21 Credentials Package Control Evidence

Date: 2026-07-17
Phase: P21 Signing Path Unblock Decision Or Pause Gate
Status: PASS

P21 revalidates the explicit `credentials` package lane after recording signing
as PAUSED. The credentials package remains explicit, private-trial-only, and
separate from the deterministic `base` package.

## Scope

This round validates the `credentials` package lane and restores the local
package output to `base` afterward.

It does not:

- run signing commands;
- create, import, purchase, invent, or use certificates;
- create signed artifacts;
- call timestamp services;
- approve public release;
- commit package outputs.

Credential smoke uses runtime-generated throwaway fake values. Output records
only the non-secret reference identifier `snaplex/package-credential-smoke`.

## Commands And Results

Command:

```powershell
python scripts\package_windows.py --dry-run --variant credentials
```

Result: PASS. Output reported `SNAPLEX_PACKAGE_VARIANT=credentials`.

Command:

```powershell
python scripts\package_windows.py --variant credentials
```

Result: PASS. PyInstaller output reported analysis of
`keyring.backends.Windows`, and build output remained under ignored `build\`
and `dist\` paths.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS.

Evidence from output:

- keyring backend: `keyring.backends.Windows.WinVaultKeyring`;
- credential reference: `snaplex/package-credential-smoke`;
- keyring import/backend discovery: PASS.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS.

Evidence from output:

- keyring backend: `keyring.backends.Windows.WinVaultKeyring`;
- credential reference: `snaplex/package-credential-smoke`;
- credential save/read/delete: PASS;
- credential cleanup: PASS.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
```

Result: PASS.

Evidence from output:

- keyring backend: `keyring.backends.Windows.WinVaultKeyring`;
- credential reference: `snaplex/package-credential-smoke`;
- credential save: PASS;
- credential retained for restart check.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS.

Evidence from output:

- keyring backend: `keyring.backends.Windows.WinVaultKeyring`;
- credential reference: `snaplex/package-credential-smoke`;
- credential restart readiness: PASS;
- credential cleanup: PASS.

Command:

```powershell
python scripts\package_windows.py --variant base
```

Result: PASS. Output reported `SNAPLEX_PACKAGE_VARIANT=base`, restoring the
local package output to the deterministic base lane.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result after base restore: PASS as expected rejection. The command exited with
code 1 and output reported `keyring is not available in this runtime`.

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

The `credentials` package lane remains explicit and private-trial only:

- credentials dry-run and build pass only when the `credentials` variant is
  selected;
- Windows keyring backend discovery passes in the credentials package;
- import, cycle, save, and check-delete smoke pass;
- save and check-delete were run sequentially;
- cleanup passes;
- smoke output records only a non-secret reference identifier;
- local package output is restored to base afterward;
- restored base package still rejects credential smoke;
- no raw credential values, keyring exports, package outputs, screenshots,
  logs, certificates, private keys, signed artifacts, timestamp responses,
  `.env`, local app data, tester data, OCR caches, or provider secrets are
  committed.

## Round 5 Self-Checks

Debug self-check:

- The evidence is explained by the smallest credentials-lane workflow:
  credentials dry-run/build, import, cycle, sequential save, check-delete,
  cleanup, final base restore, and base credential smoke expected rejection.
- Success, expected rejection, restart readiness, cleanup, no raw credential,
  paused signing, no-signing-command, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- Credentials package validation does not change provider, credential,
  settings, history, capture, OCR, UI, package specification, or trial
  readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free after restore.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
