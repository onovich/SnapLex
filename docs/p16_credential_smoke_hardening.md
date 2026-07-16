# P16 Credential Smoke Hardening

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: credential smoke command hardening PASS

P16 Round 4 hardens the explicit `--smoke-credentials` command so it is usable
as a production-hardening gate for the `credentials` package variant. The smoke
now uses phase-neutral local keyring identifiers and wraps credential-store
failures in concise no-secret `PackagedSmokeError` messages.

## Code Hardening

Updated smoke identifiers:

- service name: `SnapLexPackageCredentialSmoke`
- credential reference: `snaplex/package-credential-smoke`

These names replace the P15-specific package spike label in runtime code while
leaving P15 historical evidence unchanged.

Credential store failures during save, read, restart check, or cleanup now map
to sanitized packaged smoke errors:

- `credential save failed: credential source unavailable.`
- `credential read failed: credential source unavailable.`
- `credential restart readiness check failed: credential source unavailable.`
- `credential cleanup failed: credential source unavailable.`

The messages do not include raw credential values or underlying backend
exception text.

## Deterministic Test Evidence

Command:

```cmd
python -m pytest tests\test_release_smoke.py --basetemp tmp\pytest-p16-smoke-hardening
```

Result: PASS with 9 tests. Pytest emitted a non-blocking local cache warning;
no test failed.

The tests cover:

- import smoke output uses the phase-neutral reference;
- cycle smoke cleans up and does not leak raw values;
- save/check-delete restart smoke uses the same phase-neutral reference;
- smoke saves under `SnapLexPackageCredentialSmoke`;
- keyring store exceptions are wrapped without backend detail leakage;
- CLI import output does not contain `p15` or credential values.

## Source Smoke Evidence

Commands:

```cmd
python -m snaplex --smoke-credentials --credential-smoke-mode import
python -m snaplex --smoke-credentials --credential-smoke-mode cycle
python -m snaplex --smoke-credentials --credential-smoke-mode save
python -m snaplex --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS when run in valid order. The first attempted parallel
save/check-delete check produced an expected missing result because
`check-delete` must run after `save`; the sequential rerun passed and cleaned
up the keyring reference.

Observed successful output included:

```text
credential reference: snaplex/package-credential-smoke
credential save/read/delete: PASS
credential restart readiness: PASS
credential cleanup: PASS
```

## Packaged Smoke Evidence

The credentials package was rebuilt after the code hardening:

```cmd
python scripts\package_windows.py --variant credentials
```

Result: PASS.

Observed build evidence included:

```text
SNAPLEX_PACKAGE_VARIANT=credentials
Processing standard module hook 'hook-keyring.py'
Analyzing hidden import 'keyring.backends.Windows'
Processing standard module hook 'hook-pywintypes.py'
Build complete! The results are available in: D:\ToolProjects\SnapLex\dist
```

Packaged smoke commands:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS.

Observed packaged output included:

```text
credential reference: snaplex/package-credential-smoke
keyring backend: keyring.backends.Windows.WinVaultKeyring
credential save/read/delete: PASS
credential restart readiness: PASS
credential cleanup: PASS
```

Cleanup confirmation:

```cmd
python -c "<source status check for package credential smoke reference>"
```

Result: PASS.

```text
post_p16_smoke_status=missing
```

## No-Secret Guarantees

- Smoke values are runtime-generated throwaway strings and are never printed.
- Smoke output records only backend labels, mode names, and the non-secret
  keyring reference.
- Failure wrapping intentionally omits backend exception text.
- The source and packaged restart checks leave
  `snaplex/package-credential-smoke` missing after cleanup.
- Generated package outputs and smoke data remain ignored local artifacts.

## Round 4 Self-Checks

Debug self-check:

- The current change is explained by the smallest credential smoke workflows:
  import, cycle, save, check-delete, error wrapping, and cleanup status.
- Success, expected missing when run out of order, unavailable backend wrapping,
  restart readiness, cleanup, and no-secret states are covered.
- Tester-facing setup and cleanup prose is deferred to Round 5.

Architecture self-check:

- Credential behavior remains behind `CredentialService` and
  `KeyringCredentialStore`.
- The `credentials` package remains explicit; base package behavior is not
  changed.
- Provider calls remain behind provider registry and `TranslationPipeline`; no
  real-provider network smoke was introduced.
