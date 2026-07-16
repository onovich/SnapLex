# P12 Credential Package Variant Decision

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: deferred for first private pilot

P12 decides whether SnapLex should build a credential-capable package variant
for the first private pilot. This decision does not implement a new package
variant.

## Decision

Do not build or promise a credential-capable package variant for the first P12
private pilot.

Keep the supported pilot paths as:

- deterministic `base` package for fake smoke, launch, Settings, History, and
  package workflow validation;
- source checkout plus `.[gui,credentials]` for local secure credential testing
  when `keyring` is installed;
- environment variables for optional real-provider source/package trials;
- future credential-capable package variant deferred until a later explicit
  phase.

## Rationale

The first private pilot needs safe feedback loops more than another package
surface. Packaging keyring support now would add dependency, installer,
Windows Credential Locker, cleanup, and support questions before manual
credential smoke has passed in this executor environment.

The current environment reports:

```text
missing
```

for the optional `keyring` package. P11 and P12 should not turn a missing,
optional, source-only secure credential path into a packaged release promise.

## Validation

Base package dry-run:

```cmd
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS.

```text
SNAPLEX_PACKAGE_VARIANT=base
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Full capture/OCR dry-run:

```cmd
python scripts\package_windows.py --dry-run --variant full
```

Result: PASS. This remains a capture/OCR dependency variant and does not imply
keyring support.

Focused tests:

```cmd
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py tests\test_credentials.py --basetemp tmp\pytest-p12-credential-package
```

Result: PASS with 23 tests.

## Conditions For A Future Credential-Capable Package

A later P13 or post-P12 phase may build a credential-capable package only after
all of these are true:

- optional `keyring` support is installed in the package build environment;
- PyInstaller hidden imports or backend modules are deliberately identified;
- Windows Credential Locker save/read/delete works from the packaged executable
  with a throwaway fake value;
- Settings credential readiness survives package restart without displaying
  the secret;
- package failure states remain clear when the local keyring backend is missing
  or unavailable;
- uninstall/cleanup guidance for local credentials is documented;
- artifact and secret scans prove no keyring exports, `.env`, logs, local app
  data, screenshots, package outputs, OCR caches, or provider secrets are
  tracked.

## Pilot Guidance

For the first private pilot:

- use `StartPackagedFakeTrial.cmd` and `SmokeTrial.cmd` for package confidence;
- use `StartPackagedTrial.cmd` only with environment variables or accepted
  endpoints already configured;
- use source checkout plus `python -m pip install -e ".[gui,credentials]"` for
  local secure credential experiments;
- classify requests for packaged keyring support as `defer` unless they block a
  specifically approved credential-package pilot.

## Explicit Non-Promise

The P12 base package does not promise:

- packaged keyring support;
- provider account sign-in;
- SnapLex Cloud;
- OAuth, billing, or hosted token broker;
- automatic credential migration from source checkout to package.
