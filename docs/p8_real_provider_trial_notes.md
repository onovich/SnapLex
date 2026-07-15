# P8 Real Provider Trial Notes

Date: 2026-07-15
Phase: P8 Provider Setup And Real Translation UX
Status: hardening notes

P8 makes real-provider trial setup visible in Settings, but it does not add
SnapLex Cloud, account OAuth, a backend token broker, billing, or raw API-key
persistence.

## Credential Rules

- Store provider names, provider order, endpoints, model names, timeout/retry
  values, and API-key environment variable names.
- Do not store raw API key values in `config.json`, history, docs, tests, logs,
  screenshots, package resources, or smoke output.
- Settings may show whether an env var is present in the current process, but
  not the value.
- `Test Connection` may send the probe text to the selected real provider only
  when the user clicks it and local provider configuration exists.
- Automated tests use mocked HTTP transports only.

## Real Trial Paths

Source real-provider trial:

```cmd
StartTrial.cmd
```

Packaged real-provider trial:

```cmd
StartPackagedTrial.cmd
```

Both commands call `RequireRealProvider.cmd`. If no OpenAI, DeepL, or
LibreTranslate configuration is present, they exit with a clear setup message
instead of silently switching to fake.

## Fake Smoke Paths

Source fake smoke:

```cmd
StartFakeTrial.cmd --no-gui
```

Packaged fake smoke:

```cmd
StartPackagedFakeTrial.cmd --no-gui
```

Trial smoke:

```cmd
SmokeTrial.cmd
```

Fake mode is deterministic and offline. It is for UI/package smoke and should
be visibly labeled as fake smoke mode in result states.

## Optional Manual Real Provider Smoke

Run only when local credentials or a self-hosted endpoint already exist:

1. Set one provider configuration in the shell environment.
2. Run `StartTrial.cmd`.
3. Open `Settings`.
4. Select the provider and confirm readiness shows the configured env var or
   endpoint.
5. Click `Test Connection`.
6. Translate a short clipboard phrase.
7. Confirm result provider identity is the selected real provider, not fake.
8. Close the app and confirm no `.env`, `config.json`, `history.json`, logs, or
   screenshots containing secrets were created in tracked paths.

Do not paste provider secrets into issues, docs, screenshots, or chat logs.

## Future Secure Credential Work

Future secure credential work belongs outside P8. Candidate directions:

- OS keychain integration for local desktop secrets.
- SnapLex Cloud token broker for providers that require server-side secrets.
- Enterprise/resource identity flows where provider APIs support them.
- Explicit account and billing design before any OAuth-style sign-in appears as
  enabled UI.

Until then, environment variables remain the supported local secret boundary.

