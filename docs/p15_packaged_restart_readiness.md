# P15 Packaged Restart Readiness

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: packaged restart readiness PASS

P15 Round 5 proves that a credential saved by one packaged SnapLex process can
be detected by a second packaged process and then cleaned up, without printing
or displaying the throwaway value.

## Packaged Save Process

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
```

Result: PASS.

Observed output:

```text
SnapLex packaged credential smoke PASS
- credential smoke mode: save
- keyring backend: keyring.backends.Windows.WinVaultKeyring
- credential reference: snaplex/p15/package-spike
- credential save: PASS
- credential retained for restart check
```

## Packaged Check/Delete Process

Command:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS.

Observed output:

```text
SnapLex packaged credential smoke PASS
- credential smoke mode: check-delete
- keyring backend: keyring.backends.Windows.WinVaultKeyring
- credential reference: snaplex/p15/package-spike
- credential restart readiness: PASS
- credential cleanup: PASS
```

The check/delete command runs in a separate process after the save command. It
confirms the credential reference is ready, resolves a non-empty value without
printing it, deletes the credential, and verifies cleanup.

## Cleanup Confirmation

Command:

```cmd
python -c "from snaplex.credentials import CredentialSource, CredentialService, KeyringCredentialStore, keyring_credential_reference; ref=keyring_credential_reference('openai','snaplex/p15/package-spike'); status=CredentialService({CredentialSource.KEYRING: KeyringCredentialStore(service_name='SnapLexP15PackageSmoke')}).status(ref); print('post_restart_status=' + status.code.value)"
```

Result: PASS.

```text
post_restart_status=missing
```

## Deterministic Test Evidence

Command:

```cmd
python -m pytest tests\test_release_smoke.py --basetemp tmp\pytest-p15-restart-readiness
```

Result: PASS with 7 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

## No-Secret Evidence

- The saved value is generated at runtime and never printed.
- The output records only the non-secret reference identifier.
- The second process deletes the credential before exiting.
- No keyring export, `.env`, provider secret, package output, smoke data, local
  config/history, screenshot, log, OCR cache, or tester personal data is
  staged.

## Round 5 Self-Checks

Debug self-check:

- The current change is explained by packaged restart readiness.
- Save, separate-process check, delete, cleanup, no-secret, and fail-closed
  states are covered.
- The smoke leaves the keyring reference missing after completion.

Architecture self-check:

- Credential behavior stays behind `CredentialService` and
  `KeyringCredentialStore`.
- The base package and fake trial path are unchanged.
- P15 still records spike evidence rather than promising production packaged
  credential support.
