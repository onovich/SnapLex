# P15 Packaged Keyring Import Evidence

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: packaged keyring import/backend discovery PASS

P15 Round 3 added an explicit credential package smoke entry point and used the
explicit `credentials` package variant to prove keyring import and Windows
backend discovery inside the packaged executable. This is spike evidence only;
it does not make credential-capable packaging the base package or a production
release promise.

## Implementation Boundary

New explicit smoke surface:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

The CLI calls `snaplex.release_smoke.run_packaged_credential_smoke`, which uses
existing `CredentialService` and `KeyringCredentialStore` boundaries. Packaging
scripts remain a thin variant/hidden-import wrapper.

Supported smoke modes in source and packaged runtimes:

- `import`: import `keyring` and discover the backend only;
- `cycle`: save/read/delete with a throwaway runtime-generated value;
- `save`: save a throwaway runtime-generated value for restart-readiness smoke;
- `check-delete`: check after restart and clean up.

Round 3 uses only `import`. Save/read/delete and restart readiness are recorded
in later P15 evidence documents.

## Build Evidence

Command:

```cmd
python scripts\package_windows.py --variant credentials
```

Result: PASS.

Observed PyInstaller evidence includes:

```text
Analyzing hidden import 'keyring.backends.Windows'
Processing standard module hook 'hook-keyring.py'
Processing standard module hook 'hook-pywintypes.py'
SNAPLEX_PACKAGE_VARIANT=credentials
Build complete! The results are available in: D:\ToolProjects\SnapLex\dist
```

The generated package output is under ignored `build\` and `dist\` only.

## Packaged Runtime Evidence

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS.

Observed output:

```text
SnapLex packaged credential smoke PASS
- credential smoke mode: import
- keyring backend: keyring.backends.Windows.WinVaultKeyring
- credential reference: snaplex/p15/package-spike
- keyring import/backend discovery: PASS
```

Bootstrap control:

```cmd
dist\SnapLex\SnapLex.exe --version
```

Result: PASS, `SnapLex 0.1.0`.

## Deterministic Test Evidence

Command:

```cmd
python -m pytest tests\test_release_smoke.py tests\test_package_windows.py --basetemp tmp\pytest-p15-keyring-import-rerun
```

Result: PASS with 14 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

Command:

```cmd
python -m ruff check snaplex\app.py snaplex\release_smoke.py tests\test_release_smoke.py
```

Result: PASS.

## No-Secret And Artifact Evidence

- The import smoke does not save a credential value.
- Runtime-generated throwaway values are not printed by the smoke helper.
- The output records only the non-secret keyring reference identifier.
- No keyring export, `.env`, provider secret, package output, smoke data, local
  config/history, screenshot, log, OCR cache, or tester personal data is
  staged.
- `git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models`
  returned no tracked files.

## Round 3 Self-Checks

Debug self-check:

- The current change is explained by packaged keyring import/backend discovery.
- Import pass, backend pass, generated-output hygiene, and no-secret states are
  covered.
- Save/read/delete, restart readiness, and cleanup guidance are deferred to
  later P15 rounds.

Architecture self-check:

- The base package path remains unchanged and explicit.
- Credential behavior stays behind `CredentialService` and
  `KeyringCredentialStore`.
- Packaging changes remain limited to explicit `credentials` variant hidden
  imports and a dedicated smoke CLI.
