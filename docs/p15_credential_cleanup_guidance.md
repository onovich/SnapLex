# P15 Credential Cleanup Guidance

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: cleanup guidance ready

This guidance is for maintainers running the P15 credential-capable package
spike. It is not end-user release documentation and it does not authorize real
provider secrets in smoke artifacts.

## What P15 Creates

P15 package smoke may create:

- a local generated package under ignored `build\` and `dist\`;
- local smoke app data under ignored `snaplex-smoke-data\`;
- pytest temporary output under ignored `tmp\` and `.pytest_cache\`;
- one temporary OS keyring entry under service name
  `SnapLexP15PackageSmoke` and identifier `snaplex/p15/package-spike`.

The normal `cycle` and `check-delete` smoke modes delete the keyring entry
before exit. If a process is interrupted after `save`, use the cleanup steps
below.

## Keyring Cleanup

First, prefer SnapLex's own credential smoke cleanup path:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Expected result when a saved smoke credential exists:

```text
SnapLex packaged credential smoke PASS
- credential restart readiness: PASS
- credential cleanup: PASS
```

If the credential has already been removed, the command can fail with a missing
credential message. That is acceptable as long as a source status check confirms
the reference is missing:

```cmd
python -c "from snaplex.credentials import CredentialSource, CredentialService, KeyringCredentialStore, keyring_credential_reference; ref=keyring_credential_reference('openai','snaplex/p15/package-spike'); status=CredentialService({CredentialSource.KEYRING: KeyringCredentialStore(service_name='SnapLexP15PackageSmoke')}).status(ref); print(status.code.value)"
```

Expected clean result:

```text
missing
```

Do not export Windows Credential Locker data. Do not paste credential values,
keyring exports, screenshots of credentials, or logs into docs, commits,
issues, or chat.

## Local Package And Smoke Data Cleanup

Generated package output is ignored by git. Remove it only when you no longer
need the local smoke package:

```powershell
Remove-Item -LiteralPath .\build -Recurse -Force
Remove-Item -LiteralPath .\dist -Recurse -Force
```

Generated smoke data is also ignored. Remove only the local directories you
created for smoke:

```powershell
Remove-Item -LiteralPath .\snaplex-smoke-data -Recurse -Force
Remove-Item -LiteralPath .\tmp -Recurse -Force
```

Before running removal commands, confirm the current directory is the SnapLex
workspace and the target paths are the ignored local smoke directories. Do not
delete user data directories outside the workspace.

## Before Committing

Run:

```cmd
git status --short
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models
```

Expected result:

- `git status --short` must not include generated package outputs, smoke data,
  `.env` files, logs, keyring exports, screenshots, OCR caches, or tester
  personal data.
- `git ls-files -- ...` must print no tracked generated artifacts.

## Real Provider Reminder

P15 credential smoke uses throwaway fake values only. Optional real-provider
network smoke remains out of automated validation and may run only when local
credentials already exist and a human explicitly approves network use for that
round.

## Round 7 Self-Checks

Debug self-check:

- The current change is explained by cleanup guidance.
- Keyring cleanup, local package cleanup, smoke data cleanup, expected missing
  status, and no-secret states are covered.
- The guidance distinguishes acceptable missing cleanup from failed credential
  deletion.

Architecture self-check:

- Cleanup instructions do not move credential behavior into packaging scripts.
- The base package and explicit credential variant boundaries remain separate.
- No real provider secrets, keyring exports, logs, screenshots, smoke data, or
  package outputs are committed.
