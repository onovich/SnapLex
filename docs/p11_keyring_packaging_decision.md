# P11 Keyring Packaging Decision

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: decision recorded

## Decision

The P11 private trial keeps the deterministic `base` package as the supported
packaged smoke artifact. The base package does not require or promise OS
keyring support. It remains fake-provider safe, no-network, and suitable for
repeatable `--version`, `--no-gui`, and `--smoke-package` checks.

For private trial users who want local secure credential storage, P11 supports
the source checkout path with the optional credentials extra:

```powershell
python -m pip install -e ".[gui,credentials]"
```

A credential-capable packaged variant is deferred until a later phase because
the current executor environment does not have `keyring` installed and manual
Windows Credential Locker smoke could not be run. SnapLex should not claim
packaged keyring support until the optional dependency is bundled deliberately
and a throwaway-key Windows Credential Locker smoke passes.

## Rationale

P10 made keyring support optional and lazy so base app import, no-GUI bootstrap,
package dry-run, automated tests, and fake smoke do not require an OS keyring.
P11 preserves that boundary. Shipping the base package with unvalidated keyring
support would turn an optional local credential path into an unsupported release
promise.

The safest private trial packaging stance is:

- `base`: supported deterministic package and smoke path;
- `capture`, `ocr`, `full`: optional capture/OCR dependency variants only;
- source checkout + `.[credentials]`: accepted local secure credential path for
  users who can install optional dependencies;
- credential-capable package: deferred until manual keyring smoke and package
  dependency inclusion are both validated.

## Validation

Base package dry-run:

```powershell
python scripts\package_windows.py --dry-run --variant base
```

Result:

```text
SNAPLEX_PACKAGE_VARIANT=base
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Full optional capture/OCR dry-run remains available and does not imply keyring
support:

```powershell
python scripts\package_windows.py --dry-run --variant full
```

Result:

```text
SNAPLEX_PACKAGE_VARIANT=full
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Focused package/release tests:

```powershell
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py --basetemp tmp\pytest-p11-package
```

Result: PASS with 8 tests.

## Private Trial Guidance

Use the packaged base artifact to validate launch, fake workflow, settings,
history, and packaged smoke. Use source checkout plus `.[credentials]` when a
tester specifically needs OS keyring storage. Use environment variables for
real-provider packaged trials until a credential-capable package is explicitly
validated.

Real packaged trial paths must continue to fail closed when no real provider
credential or accepted endpoint exists. Fake packaged trial paths must continue
to be labeled as fake smoke mode.

## Deferred Package Work

A future credential-capable package should decide and test:

- whether `keyring` and backend-specific modules need PyInstaller hidden
  imports;
- whether Windows Credential Locker works from the packaged executable;
- whether Settings save/delete/readiness survives package restart;
- whether uninstall/cleanup guidance is needed for stored local credentials;
- whether keyring failures are still clear and non-fatal in the package.

No package outputs, binaries, local app data, screenshots, logs, keyring
exports, `.env`, or provider secrets should be committed.
