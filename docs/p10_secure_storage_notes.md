# P10 Secure Storage Notes

Date: 2026-07-15
Phase: P10 Secure Credential And Account Strategy
Status: implemented local secure storage notes

P10 adds an optional local secure credential path without changing SnapLex into
a cloud account product. The secure storage rule is simple: SnapLex config may
store where to find a credential, but not the credential value.

## Stored In SnapLex Config

Provider config may store these non-secret fields:

- provider name and provider order;
- endpoint/base URL;
- model/options;
- timeout and retry values;
- `api_key_env_var`;
- `credential_source`;
- `credential_identifier`.

The `credential_identifier` is a lookup id, such as
`snaplex/openai/default`. It is not a provider secret.

## Never Stored By SnapLex

SnapLex must not store raw provider secrets in:

- `config.json`;
- `history.json`;
- docs, tests, fixtures, screenshots, logs, or smoke output;
- package resources;
- `.env` files in git;
- generated package, smoke, OCR model, or keyring export artifacts.

## Environment Variable Storage

The environment path is read-only inside SnapLex. Users set values such as
`SNAPLEX_OPENAI_API_KEY` in their shell or ignored launcher, and SnapLex stores
only the variable name. Settings may report that the variable is present, but it
must never display the value.

## OS Keyring Storage

The keyring path uses the optional `credentials` extra:

```powershell
python -m pip install -e ".[gui,credentials]"
```

`KeyringCredentialStore` imports `keyring` only when a keyring credential is
used. App import, `python -m snaplex --no-gui`, package dry-run, and automated
tests do not require a real keyring backend.

Settings may collect a secret only in a password-style transient input. After a
save/delete/test operation, the input field must be cleared and status text must
describe only the credential source and readiness.

## Automated Test Boundary

Automated tests use `InMemoryCredentialStore`, injected fake keyring modules, or
environment mappings. They must not require:

- a real OS keyring;
- provider credentials;
- provider network calls;
- model downloads;
- screen permissions.

## Optional Manual Windows Credential Locker Smoke

Run this only with a throwaway credential value:

1. Install `.[gui,credentials]`.
2. Set `SNAPLEX_APP_DATA_DIR` to a temporary directory.
3. Set `SNAPLEX_PROVIDER` and `SNAPLEX_PROVIDER_ORDER` to a real provider name.
4. Set `SNAPLEX_<PROVIDER>_CREDENTIAL_SOURCE=keyring`.
5. Set a non-secret `SNAPLEX_<PROVIDER>_CREDENTIAL_IDENTIFIER`.
6. Launch `python -m snaplex`.
7. Save the throwaway value in Settings.
8. Relaunch and confirm readiness reports the reference, not the value.
9. Delete the credential from Settings.
10. Confirm no tracked file contains the value or generated local data.

Manual keyring smoke was not required for P10 automated acceptance and remains a
recommended P11 release-hardening task.
