# P16 Credentials Variant Hardening

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: credentials variant build and dependency gate PASS

P16 Round 3 proves that the explicit `credentials` package variant remains the
only credential-capable package build path and that its optional dependency
surface is visible in the build, dry-run, packaged import smoke, and tests.

## Variant Boundary

The credential-capable package is built only when the maintainer asks for the
explicit variant:

```cmd
python scripts\package_windows.py --variant credentials
```

The default remains:

```cmd
python scripts\package_windows.py --variant base
```

P16 does not change the default package variant and does not silently add
keyring support to the base package.

## Credentials Variant Build Evidence

Command:

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

The generated package output is local and ignored under `build\` and `dist\`.

## Dry-Run Gate

Credentials dry-run:

```cmd
python scripts\package_windows.py --dry-run --variant credentials
```

Result: PASS.

```text
SNAPLEX_PACKAGE_VARIANT=credentials
```

Base dry-run control:

```cmd
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS.

```text
SNAPLEX_PACKAGE_VARIANT=base
```

## Packaged Import Smoke

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

The output records backend and non-secret reference information only. No raw
credential value is created or printed in import mode.

## Focused Test Evidence

Command:

```cmd
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py --basetemp tmp\pytest-p16-credentials-variant
```

Result: PASS with 14 tests. Pytest emitted a non-blocking local cache warning;
no test failed.

The tests confirm:

- `credentials` remains a named explicit variant;
- tracked spec hidden imports include `keyring.backends.Windows`;
- non-credential variants exclude keyring modules;
- packaged credential import/cycle/restart smoke goes through
  `CredentialService` and does not leak raw values.

## Hardening Finding For Round 4

The dependency gate passes. The remaining smoke-hardening work is to make the
credential smoke reference and service label phase-neutral, so future private
trial docs are not tied to the P15 spike name. That change belongs in Round 4
with deterministic tests for output and cleanup.

## Round 3 Self-Checks

Debug self-check:

- The current evidence is explained by the smallest credentials package
  dependency workflow: explicit variant build, dry-run, packaged import smoke,
  and focused tests.
- Success, explicit variant, optional dependency import, backend discovery,
  base control, generated-output hygiene, and no-secret states are covered.
- Save/read/delete, restart readiness, and smoke output naming hardening are
  deferred to Round 4.

Architecture self-check:

- The explicit `credentials` variant remains the only credential-capable
  package path.
- The base package remains deterministic and keyring-free.
- Credential behavior stays behind `CredentialService` and
  `KeyringCredentialStore`; packaging only selects hidden imports for the
  explicit variant.
