# P11 Keyring Smoke Evidence

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: manual OS keyring smoke blocked by missing optional dependency

P11 attempted to validate the local secure credential path before broader
private trial distribution. The current executor Python environment does not
have the optional `keyring` package installed, so a real Windows Credential
Locker smoke could not be run in this session.

## Environment Check

Command:

```powershell
python -c "import importlib.util; print('keyring' if importlib.util.find_spec('keyring') else 'missing')"
```

Result:

```text
missing
```

Exact blocker: the optional `credentials` dependency group is not installed in
the current executor environment. P11 did not download dependencies or install
new packages because automated validation must remain deterministic and
no-network.

## Lazy Unavailable Smoke

The accepted P10 boundary was checked to make sure missing keyring support is a
controlled unavailable state, not an app bootstrap crash:

```powershell
python -c "from snaplex.credentials import create_default_credential_service, keyring_credential_reference; status=create_default_credential_service(include_keyring=True).status(keyring_credential_reference('openai','snaplex/p11/throwaway')); print(status.code.value); print(status.status_text); print(status.detail_text)"
```

Result:

```text
unavailable
Credential source unavailable
Install the optional credentials extra to use local secure storage.
```

No throwaway credential value was saved, printed, or persisted.

## Focused Automated Coverage

Command:

```powershell
python -m pytest tests\test_credentials.py tests\test_settings_service.py tests\test_provider_setup.py --basetemp tmp\pytest-p11-keyring
```

Result: PASS with 37 tests.

The focused tests cover:

- in-memory fake keyring store save/resolve/delete;
- injected fake keyring module behavior;
- unavailable keyring backend status;
- Settings save/delete credential paths through services;
- provider setup ready/missing/unavailable keyring states;
- no raw secret values in repr/config/status surfaces.

## Manual Smoke Procedure For A Credential-Capable Environment

Run only with a throwaway fake value:

1. Install optional support: `python -m pip install -e ".[gui,credentials]"`.
2. Set `SNAPLEX_APP_DATA_DIR` to a temporary directory.
3. Set `SNAPLEX_PROVIDER=openai` and `SNAPLEX_PROVIDER_ORDER=openai`.
4. Set `SNAPLEX_OPENAI_CREDENTIAL_SOURCE=keyring`.
5. Set `SNAPLEX_OPENAI_CREDENTIAL_IDENTIFIER=snaplex/p11/throwaway`.
6. Launch `python -m snaplex`.
7. In Settings, save a throwaway value in the local secret field.
8. Confirm readiness reports a keyring reference/status, not the value.
9. Close and relaunch with the same app data directory.
10. Confirm readiness persists without displaying the value.
11. Delete the credential.
12. Confirm `git status --short --branch` does not include app data,
    screenshots, logs, keyring exports, `.env`, package outputs, or secrets.

## Trial Impact

For this private trial baseline, environment variables remain the reliable
real-provider credential path. Keyring setup is documented and service-tested,
but should not be promised as packaged release behavior until the optional
dependency is installed and Windows Credential Locker smoke passes with a
throwaway value.
