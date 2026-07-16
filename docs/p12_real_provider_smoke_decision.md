# P12 Real Provider Smoke Decision

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: intentionally skipped for automated P12 validation

P12 does not run real-provider smoke by default. Real-provider smoke may make
network calls and may use paid or rate-limited provider credentials. It is
allowed only when local credentials already exist and a human intentionally
approves the network use for that round.

## Decision

Real-provider smoke is intentionally skipped for this P12 executor pass.

Reasons:

- no real provider credential or accepted endpoint is configured in the current
  executor environment;
- no human approval was given to run provider network calls;
- P12 automated validation must remain deterministic, no-network, and
  no-secret;
- fake smoke and fail-closed real trial paths already cover the private-pilot
  safety gates.

## Evidence

No-network readiness check:

```cmd
python -m snaplex --check-real-provider
```

Result: expected rejection PASS.

```text
Real translation provider is not configured.
```

Real trial command guardrail:

```cmd
StartTrial.cmd --no-gui
```

Result: expected rejection PASS. The command printed setup examples with
`your_trial_key` placeholders and did not fall back to fake translation.

## Policy For Future Manual Real-Provider Smoke

Run at most one narrow real-provider smoke during the first private pilot, and
only if all conditions are true:

- the tester or release owner already has a local private-trial provider key or
  accepted self-hosted endpoint;
- the key is separate from personal/production use;
- the provider account has the lowest practical quota, budget, and access;
- the tester explicitly approves the network call for this smoke;
- no raw key value is pasted into docs, screenshots, feedback, logs, commits,
  package resources, or chat;
- the test uses synthetic text only, such as `hello`;
- the smoke result is summarized without provider response payloads.

## Future Runbook

Use environment variables or local secure credential references only. Example
for an environment variable path:

```powershell
$env:SNAPLEX_OPENAI_API_KEY = "<local_private_trial_key>"
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai"
python -m snaplex --check-real-provider
StartTrial.cmd
```

Use `Test Connection` in Settings only when the tester intentionally approves
the network call. After smoke:

1. remove shell environment variables from open terminals;
2. revoke or rotate the trial key if it was shared;
3. confirm no `.env`, logs, screenshots, config/history files, keyring exports,
   package outputs, or provider secrets are tracked;
4. record only provider name, mode, command, expected result, actual result, and
   whether the smoke blocks the pilot.

## Expected Failure Without Credentials

When no real provider is configured, source and packaged real trial paths must
fail closed:

```cmd
StartTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

```text
Real translation provider is not configured.
```

This fail-closed behavior is a required private-pilot safety gate.
