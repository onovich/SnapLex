# P24 Credentials Package Candidate Evidence

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: explicit credentials package candidate lane revalidated; base lane restored

P24 revalidated the explicit `credentials` package candidate lane with
runtime-generated throwaway credential smoke. After credentials smoke, P24
rebuilt the deterministic `base` package and confirmed it remains keyring-free.

## Commands

```cmd
python scripts\package_windows.py --dry-run --variant credentials
python scripts\package_windows.py --variant credentials
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
python scripts\package_windows.py --variant base
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
git status --short --ignored
```

## Results

| Check | Result |
| --- | --- |
| Credentials package dry-run | PASS; reported `SNAPLEX_PACKAGE_VARIANT=credentials`. |
| Credentials package build | PASS; PyInstaller included keyring hooks and completed local ignored output under `dist\SnapLex`. |
| Credentials import smoke | PASS; reported `keyring.backends.Windows.WinVaultKeyring` and `snaplex/package-credential-smoke`. |
| Credentials cycle smoke | PASS; save/read/delete and cleanup passed. |
| Credentials save smoke | PASS; credential retained for restart check. |
| Credentials check-delete smoke | PASS; restart readiness and cleanup passed. |
| Base package restore build | PASS; rebuilt package reported `SNAPLEX_PACKAGE_VARIANT=base`. |
| Final base credential smoke | PASS as expected rejection; exited 1 with `keyring is not available in this runtime.` |

## Credential Safety

The smoke path used only runtime-generated throwaway credential values. Output
recorded only:

- credential smoke mode;
- keyring backend;
- non-secret credential reference `snaplex/package-credential-smoke`;
- pass/fail status for import, save/read/delete, restart readiness, and
  cleanup.

No raw credential value, provider API key, `.env` content, keyring export,
provider dashboard content, local config/history file, or real provider account
data was printed, stored in docs, staged, or committed.

## Candidate Interpretation

The credentials candidate remains support-ready only as an explicit
private-trial lane:

- it must be built with `--variant credentials`;
- it must be labeled `unsigned-private-trial`;
- it is not a signed archive, installer, updater, release feed, public release,
  or silently merged base package;
- it must use throwaway generated values for smoke;
- it must be followed by base restore or base-lane revalidation before the
  deterministic base candidate is considered clean.

## Base Restore Confirmation

After credentials smoke, P24 rebuilt the base package and reran credential
import smoke. The final base package rejected keyring use with:

```text
SnapLex packaged credential smoke FAIL: keyring is not available in this runtime.
```

This is the expected deterministic base behavior. Credential-capable support
therefore remains isolated to the explicit `credentials` variant.

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

No nonignored package output, screenshot, log, local app data, smoke data, OCR
cache, certificate, private key, signed binary, timestamp response, keyring
export, `.env` file, provider secret, or tester personal data was staged or
committed by the credentials package candidate validation.

## Round 6 Self-Checks

Debug self-check:

- The credentials candidate evidence covers dry-run, build, backend import,
  cycle, save, check-delete, base restore, final base expected rejection, and
  ignored artifact state.
- Success, expected rejection, backend discovery, throwaway credential, cleanup,
  base restore, unsupported base keyring, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- The `credentials` package remains explicit and private-trial only.
- The `base` package remains deterministic and keyring-free after restoration.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- No raw credential storage, public release, signing, certificate, installer,
  updater, release feed, cloud/account, browser, AI summary, global hotkey,
  provider rewrite, OCR/capture rewrite, full localization, signed artifact,
  timestamp response, or signing log is introduced.
