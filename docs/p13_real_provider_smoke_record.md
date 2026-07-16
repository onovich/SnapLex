# P13 Real Provider Smoke Record

Date: 2026-07-16
Phase: P13 Private Trial Feedback Response And Credential Package Feasibility
Status: intentionally skipped; fail-closed readiness PASS

P13 did not run a real provider network smoke. The executor environment did not
have a configured real provider, and no human explicitly approved a network
trial with existing local credentials for this round. This is the required safe
path from the P12/P13 policy: do not invent credentials, do not call the
network, and do not silently fall back to fake as if it were real translation.

## Result Summary

| Check | Result | Notes |
| --- | --- | --- |
| Real provider network smoke | SKIPPED | No configured real provider and no explicit human network approval for P13 Round 5. |
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

The optional real-provider smoke remains skipped for P13. A future real-provider
smoke may run only when all of these are true:

- a local real-provider credential already exists;
- a human explicitly approves network use for that round;
- the command output and any report redact secrets and private content;
- fake and real trial paths remain visibly separate;
- automated validation remains no-network and deterministic.

## Round 5 Self-Checks

Debug self-check:

- The result is tied to P13 optional real-provider smoke evidence.
- No network call was attempted.
- No raw provider key, `.env` file, API response, log, screenshot, or tester
  data was created or staged.

Architecture self-check:

- Provider execution remains behind `TranslationPipeline` and provider
  adapters; no UI or script code was changed.
- Real trial readiness remains fail-closed without silently falling back to fake
  as real translation.
- Fake smoke remains available only as labeled smoke/dev behavior.
