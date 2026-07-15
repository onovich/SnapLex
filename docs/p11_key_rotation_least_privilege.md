# P11 Key Rotation And Least Privilege Notes

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: private-trial guidance

P11 keeps provider credentials local. SnapLex does not provide production
account sign-in, billing, SnapLex Cloud, OAuth, or a hosted token broker. Private
trial testers who use real providers should treat every provider key as a
short-lived local trial secret.

## Least-Privilege Baseline

- Use a separate provider project, account, or key for SnapLex private trial
  runs. Do not reuse a personal production key.
- Prefer low quota, low budget, and short-lived trial credentials where the
  provider account supports those controls.
- Give the key only the provider access needed for translation requests. Avoid
  broad admin, account-management, billing, or unrelated model/service access.
- Prefer a provider-side usage cap or alert before handing a trial build to
  another tester.
- For LibreTranslate, prefer a local or self-hosted endpoint with a throwaway
  key when the instance requires authentication. Do not point private trial
  builds at a shared production endpoint unless that endpoint is intentionally
  approved for the trial.
- Keep endpoint URLs, provider order, and key identifiers in config; keep raw
  keys only in shell environment variables or the optional local OS keyring.

## Rotation Checklist

1. Create a replacement trial key in the provider account.
2. Update only the local secret source:
   - Environment variable path: update the shell or ignored local launcher value.
   - Local secure credential path: save the new key through Settings using the
     same non-secret credential identifier, or choose a new identifier and save
     Settings.
3. Run the no-network readiness check:

   ```cmd
   python -m snaplex --check-real-provider
   ```

4. Run `Test Connection` only when you intentionally want a provider network
   call.
5. Revoke or disable the old key in the provider account.
6. Clear old local values from open shells, ignored launchers, and local secret
   managers.
7. Rerun the fake smoke path if the goal is release/package confidence:

   ```cmd
   .\SmokeTrial.cmd
   ```

## Environment Variable Cleanup

For a PowerShell session, remove old values before setting a replacement:

```powershell
Remove-Item Env:\SNAPLEX_OPENAI_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\SNAPLEX_DEEPL_API_KEY -ErrorAction SilentlyContinue
$env:SNAPLEX_OPENAI_API_KEY = "<replacement_trial_key>"
```

Use ignored local launchers or a local secret manager if repeated manual entry is
too error-prone. Do not add raw keys to `.env.example`, docs, issues, screenshots,
commits, logs, chat, package resources, or test fixtures.

## Local Secure Credential Cleanup

When using the optional `keyring` path from source:

1. Open Settings.
2. Select the provider tab.
3. Set `Credential Source` to `Local secure credential`.
4. Use `Delete` to remove the old stored credential.
5. Paste the replacement key into the password-style local secret field.
6. Save and rerun `python -m snaplex --check-real-provider`.

SnapLex stores only the non-secret credential identifier in config. The raw key
value must remain in the local OS keyring only.

## Suspected Exposure Response

If a real provider key may have been copied into a committed file, screenshot,
log, package, issue, or chat:

1. Revoke the provider key immediately in the provider account.
2. Create a replacement trial key with reduced scope or quota.
3. Remove the leaked value from local files and ignored launchers.
4. Confirm `git status --short` and `git diff --check` are clean before any new
   release commit.
5. Prefer fake smoke commands until the replacement key has passed readiness and
   an intentional manual `Test Connection`.

P11 automated validation must remain no-network and must never require real
provider credentials.
