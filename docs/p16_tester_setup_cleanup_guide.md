# P16 Credential Package Tester Setup And Cleanup Guide

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: tester-facing setup and cleanup guidance ready

This guide is for controlled private-trial use of the explicit SnapLex
credential-capable package path. It is not a public release announcement. The
base package remains the deterministic fake-smoke package, and credential
support is available only in the explicit `credentials` variant.

## Safety Rules

- Do not paste provider API keys, bearer tokens, `.env` files, keyring exports,
  private documents, screenshots containing sensitive content, or personal data
  into issues, chat, docs, commits, or logs.
- Do not export Windows Credential Locker data.
- Do not screenshot credential fields or provider dashboards.
- Use only runtime-generated throwaway values for package credential smoke.
- Run real-provider translation smoke only when local credentials already exist
  and a human explicitly approves network use for that session.
- Keep generated package outputs, smoke data, screenshots, local app data, and
  logs outside git.

## Maintainer Setup

Install package dependencies in the local source environment:

```powershell
python -m pip install -e ".[gui,package,credentials]"
```

Build the deterministic base package when validating the default path:

```powershell
python scripts\package_windows.py --variant base
```

Build the explicit credential-capable package only when validating the
credential path:

```powershell
python scripts\package_windows.py --variant credentials
```

Expected result:

- `SNAPLEX_PACKAGE_VARIANT=credentials` appears in build output.
- PyInstaller analyzes `keyring.backends.Windows`.
- The package output is local under `dist\SnapLex`.
- The package output is not committed.

## Maintainer Smoke Before Sharing

Run the credential package smoke with no real provider secret:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Expected result:

- `import` reports `keyring.backends.Windows.WinVaultKeyring`.
- `cycle` reports save/read/delete and cleanup PASS.
- `save` reports the credential is retained for restart check.
- `check-delete` reports restart readiness and cleanup PASS.
- Output includes `snaplex/package-credential-smoke`.
- Output never includes a raw credential value.

Run the base package preservation control when switching back to base:

```cmd
python scripts\package_windows.py --variant base
cmd /c SmokeTrial.cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
cmd /c StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Expected result:

- base fake smoke passes;
- packaged real trial rejects missing real-provider setup;
- base credential smoke fails with
  `keyring is not available in this runtime`.

## Private Tester Setup

For a private tester receiving a credential-capable build:

1. Extract the provided `SnapLex` package into a local trial folder.
2. Keep the package folder outside any synced repository.
3. Run `SnapLex.exe --version`.
4. Run `SnapLex.exe --no-gui`.
5. Run `SnapLex.exe --smoke-credentials --credential-smoke-mode import`.
6. If the maintainer asks for credential smoke, run `cycle`.
7. Do not run real translation unless the maintainer has explicitly asked you
   to use your own provider account and approved network use.

Expected result:

- version and no-gui commands pass;
- credential import smoke reports a local keyring backend;
- cycle smoke reports save/read/delete and cleanup PASS;
- no command asks you to paste a provider key into logs or feedback.

## If Real Provider Testing Is Approved

Use SnapLex Settings to configure a provider and choose a credential source.
The app should show readiness and connection status without showing the raw
secret.

Feedback may include:

- provider name;
- credential source type, such as environment variable or local secure
  credential;
- readiness status text;
- connection success/failure category.

Feedback must not include:

- the provider key value;
- environment file contents;
- keyring exports;
- provider dashboard screenshots;
- private text being translated.

## Cleanup

First try the SnapLex credential smoke cleanup command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

If a saved smoke credential exists, expected result:

```text
credential restart readiness: PASS
credential cleanup: PASS
```

If the credential is already gone, `check-delete` may report missing. Confirm
cleanup from source with:

```cmd
python -c "from snaplex.credentials import CredentialSource, CredentialService, KeyringCredentialStore, keyring_credential_reference; from snaplex.release_smoke import CREDENTIAL_SMOKE_IDENTIFIER, CREDENTIAL_SMOKE_SERVICE_NAME; ref=keyring_credential_reference('openai', CREDENTIAL_SMOKE_IDENTIFIER); status=CredentialService({CredentialSource.KEYRING: KeyringCredentialStore(service_name=CREDENTIAL_SMOKE_SERVICE_NAME)}).status(ref); print(status.code.value)"
```

Expected clean result:

```text
missing
```

Historical P15 smoke used service `SnapLexP15PackageSmoke` and reference
`snaplex/p15/package-spike`. If a maintainer interrupted an old P15 `save`
smoke, use `docs/p15_credential_cleanup_guidance.md` for that legacy cleanup
reference.

## Local Files To Remove

Maintainers may remove generated package and smoke folders after validation:

```powershell
Remove-Item -LiteralPath .\build -Recurse -Force
Remove-Item -LiteralPath .\dist -Recurse -Force
Remove-Item -LiteralPath .\snaplex-smoke-data -Recurse -Force
Remove-Item -LiteralPath .\tmp -Recurse -Force
```

Before running deletion commands, confirm the current directory is the SnapLex
workspace and the target paths are local generated folders. Do not delete user
data directories outside the workspace.

## Before Sending Feedback Or Committing

Run:

```cmd
git status --short
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models
```

Expected result:

- no generated package outputs, smoke data, screenshots, `.env`, logs, keyring
  exports, OCR caches, tester personal data, or provider secrets are staged;
- the `git ls-files` command prints no tracked generated artifacts.

## Round 5 Self-Checks

Debug self-check:

- The guidance covers setup, import smoke, cycle smoke, restart cleanup,
  already-missing cleanup, legacy P15 cleanup, local generated file cleanup,
  feedback rules, and real-provider approval boundaries.
- Success, expected rejection, cleanup, and no-secret states are covered.

Architecture self-check:

- The guide does not move credential rules into UI or packaging scripts.
- Base and credentials package paths stay separate.
- Real-provider network testing remains optional, manual, and explicitly
  approved only.
