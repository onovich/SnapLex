# P22 Credentials Package Continuity Evidence

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: explicit credentials package lane revalidated

P22 revalidated the explicit `credentials` package lane and then restored the
deterministic `base` package lane. The credentials lane remains private-trial
only and uses runtime-generated throwaway smoke values.

## Commands And Results

### Credentials Package Dry-Run

Command:

```cmd
python scripts\package_windows.py --dry-run --variant credentials
```

Result: PASS.

Evidence:

- Dry-run printed the expected PyInstaller command.
- Dry-run reported `SNAPLEX_PACKAGE_VARIANT=credentials`.

### Credentials Package Build

Command:

```cmd
python scripts\package_windows.py --variant credentials
```

Result: PASS.

Evidence:

- PyInstaller completed successfully.
- Output was written under local ignored `dist\SnapLex`.
- Build output reported `SNAPLEX_PACKAGE_VARIANT=credentials`.
- PyInstaller processed `hook-keyring.py`.
- PyInstaller analyzed hidden import `keyring.backends.Windows`.
- PyInstaller analyzed hidden imports `keyring.backends.chainer` and
  `keyring.backends.null`.

### Credentials Import Smoke

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS.

Evidence:

- Output reported `SnapLex packaged credential smoke PASS`.
- Output reported `credential smoke mode: import`.
- Output reported `keyring.backends.Windows.WinVaultKeyring`.
- Output reported `credential reference: snaplex/package-credential-smoke`.
- Output reported `keyring import/backend discovery: PASS`.

### Credentials Cycle Smoke

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS.

Evidence:

- Output reported `credential smoke mode: cycle`.
- Output reported `credential save/read/delete: PASS`.
- Output reported `credential cleanup: PASS`.
- No raw credential value was printed.

### Credentials Save Smoke

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
```

Result: PASS.

Evidence:

- Output reported `credential smoke mode: save`.
- Output reported `credential save: PASS`.
- Output reported `credential retained for restart check`.
- The retained value was a runtime-generated throwaway smoke value.
- No raw credential value was printed.

### Credentials Check-Delete Smoke

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS.

Evidence:

- Output reported `credential smoke mode: check-delete`.
- Output reported `credential restart readiness: PASS`.
- Output reported `credential cleanup: PASS`.
- No raw credential value was printed.

### Final Base Restore

Command:

```cmd
python scripts\package_windows.py --variant base
```

Result: PASS.

Evidence:

- PyInstaller completed successfully.
- Output reported `SNAPLEX_PACKAGE_VARIANT=base`.
- `dist\SnapLex` was restored to the deterministic base package lane.

### Final Base Credential Smoke Control

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection.

Evidence:

- Process exited with code `1`.
- Output reported `SnapLex packaged credential smoke FAIL: keyring is not
  available in this runtime.`
- This confirms the final restored base package remains keyring-free.

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
present after credentials lane validation and final base restore.

## Decision

Credentials package continuity: PASS.

The explicit credentials package can import the Windows keyring backend and
complete throwaway credential smoke. The lane remains separate from the
deterministic base package, and the final workspace package state was restored
to `base`.

## Round 6 Self-Checks

Debug self-check:

- Dry-run, build, import, cycle, save, check-delete, final base restore, final
  base rejection, ignored output, cleanup, and no-secret states are covered.
- The `save` smoke was followed by `check-delete` before evidence was recorded.

Architecture self-check:

- The credentials package remains explicit and private-trial only.
- The base package remains deterministic and keyring-free after final restore.
- Credential behavior remains behind credential services, stores, settings,
  provider setup, and trial readiness.
- Providers remain behind the provider registry and `TranslationPipeline`.
