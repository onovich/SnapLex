# P14 Real Provider Smoke Record

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Status: intentionally skipped; fail-closed readiness PASS

P14 did not run a real provider network smoke. The executor environment did not
have a configured real provider, and no human explicitly approved a network
trial with existing local credentials for this round. This preserves the
P12/P13/P14 policy: no invented credentials, no default network calls, and no
silent fallback to fake as if it were real translation.

## Result Summary

| Check | Result | Notes |
| --- | --- | --- |
| Real provider network smoke | SKIPPED | No configured real provider and no explicit human network approval for P14 Round 7. |
| Real provider readiness | PASS expected rejection | `python -m snaplex --check-real-provider` exited non-zero with `Real translation provider is not configured.` |
| Source real trial | PASS expected rejection | `cmd /c StartTrial.cmd --no-gui` rejected missing provider setup and showed setup guidance. |
| Source fake trial control | PASS | `cmd /c StartFakeTrial.cmd --no-gui` bootstrapped in fake smoke mode and labeled it as not real translation. |

## Command Evidence

Real provider readiness:

```cmd
python -m snaplex --check-real-provider
```

Result: expected rejection PASS.

Observed output:

```text
Real translation provider is not configured.
```

Source real trial:

```cmd
cmd /c StartTrial.cmd --no-gui
```

Result: expected rejection PASS.

Observed behavior:

- reported `Real translation provider is not configured.`;
- printed real provider setup examples for OpenAI, DeepL, LibreTranslate, and
  keyring credential source;
- pointed users to `StartPackagedFakeTrial.cmd` and `StartFakeTrial.cmd` for
  packaging/smoke UI without real translation.

Source fake trial control:

```cmd
cmd /c StartFakeTrial.cmd --no-gui
```

Result: PASS.

Observed behavior:

- started SnapLex from source in fake smoke mode;
- used ignored local app data under `snaplex-smoke-data\trial-fake-source`;
- labeled provider as `fake smoke mode; this is not real translation.`;
- bootstrapped without GUI launch.

## Policy Decision

The optional real-provider smoke remains skipped for P14. A future real-provider
smoke may run only when all of these are true:

- a local real-provider credential or accepted endpoint already exists;
- a human explicitly approves network use for that round;
- command output and reports redact secrets and private content;
- fake and real trial paths remain visibly separate;
- automated validation remains no-network and deterministic.

## Round 7 Self-Checks

Debug self-check:

- The current change is explained by optional real-provider smoke evidence.
- Skipped, expected rejection, fake-control, fail-closed, no-network, and
  no-secret states are covered.
- No raw provider key, `.env` file, API response, log, screenshot, package
  output, tester data, or keyring export is created or staged.

Architecture self-check:

- Provider execution remains behind `TranslationPipeline` and provider
  adapters; no UI or script code was changed.
- Real trial readiness remains fail-closed without silently falling back to fake
  as real translation.
- Fake smoke remains available only as labeled smoke/dev behavior.
