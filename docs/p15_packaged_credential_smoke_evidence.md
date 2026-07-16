# P15 Packaged Credential Smoke Evidence

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: packaged credential save/read/delete/cleanup PASS

P15 Round 4 proves that the explicit `credentials` package can save, read,
delete, and clean up a throwaway runtime-generated credential value through
SnapLex credential service boundaries. The smoke output does not display or log
the credential value.

## Packaged Cycle Smoke

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS.

Observed output:

```text
SnapLex packaged credential smoke PASS
- credential smoke mode: cycle
- keyring backend: keyring.backends.Windows.WinVaultKeyring
- credential reference: snaplex/p15/package-spike
- credential save/read/delete: PASS
- credential cleanup: PASS
```

The output records only a non-secret keyring reference identifier. The
throwaway value is generated inside the smoke process, compared in memory,
deleted, and never printed.

## Source Control Smoke

Command:

```cmd
python -m snaplex --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS with the same backend and save/read/delete/cleanup result.

## Cleanup Confirmation

Command:

```cmd
python -c "from snaplex.credentials import CredentialSource, CredentialStatusCode, CredentialService, KeyringCredentialStore, keyring_credential_reference; ref=keyring_credential_reference('openai','snaplex/p15/package-spike'); status=CredentialService({CredentialSource.KEYRING: KeyringCredentialStore(service_name='SnapLexP15PackageSmoke')}).status(ref); print('post_cycle_status=' + status.code.value)"
```

Result: PASS.

```text
post_cycle_status=missing
```

## Deterministic Test Evidence

Command:

```cmd
python -m pytest tests\test_release_smoke.py --basetemp tmp\pytest-p15-credential-cycle
```

Result: PASS with 7 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

## No-Secret And Artifact Evidence

- No real provider secret was used.
- The throwaway value is runtime-generated and never printed by the CLI.
- The keyring reference identifier is non-secret and shared across P15 smoke
  modes for cleanup.
- No keyring export, `.env`, provider secret, package output, smoke data, local
  config/history, screenshot, log, OCR cache, or tester personal data is
  staged.
- The generated package remains under ignored `build\` and `dist\`.

## Round 4 Self-Checks

Debug self-check:

- The current change is explained by packaged credential save/read/delete smoke.
- Save, read, delete, cleanup, no-secret, source control, and packaged states
  are covered.
- Restart readiness remains deferred to Round 5.

Architecture self-check:

- Credential behavior stays behind `CredentialService` and
  `KeyringCredentialStore`.
- The smoke CLI is explicit and does not change base package behavior.
- P15 still does not promise production credential-capable package support.
