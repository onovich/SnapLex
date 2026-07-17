# P23 Base Package Continuity Evidence

Date: 2026-07-17
Phase: P23 Private Trial Feedback Intake And Support Loop Gate
Status: deterministic base package lane revalidated

P23 revalidated the deterministic `base` package lane after recording that no
external tester feedback was supplied. The base package remains the safe
private-trial path for fake smoke and no-GUI bootstrap. It is intentionally
keyring-free.

## Commands

```cmd
python scripts\package_windows.py --dry-run --variant base
python scripts\package_windows.py --variant base
StartTrial.cmd --no-gui
StartFakeTrial.cmd --no-gui
SmokeTrial.cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
git status --short --ignored
```

## Results

| Check | Result |
| --- | --- |
| Base package dry-run | PASS; reported `SNAPLEX_PACKAGE_VARIANT=base`. |
| Base package build | PASS; PyInstaller completed and wrote ignored local output under `dist\SnapLex`. |
| Source real-provider launch without provider | PASS as expected rejection; exited 1 with `Real translation provider is not configured.` |
| Source fake launch | PASS; bootstrap OK with fake smoke mode labeled as not real translation. |
| Source/package workflow smoke | PASS; `SmokeTrial.cmd` reported `SnapLex packaged workflow smoke PASS`. |
| Packaged fake launch | PASS; bootstrap OK with fake smoke mode labeled as not real translation. |
| Packaged real-provider launch without provider | PASS as expected rejection; exited 1 with `Real translation provider is not configured.` |
| Base credential smoke | PASS as expected rejection; exited 1 with `keyring is not available in this runtime.` |

## Smoke Summary

`SmokeTrial.cmd` passed with:

- `SnapLex 0.1.0`;
- no-GUI bootstrap OK;
- package variant `base`;
- settings persistence through fake provider with history enabled;
- clipboard translation smoke;
- screen fake capture/OCR translation smoke;
- history record/list/delete/clear smoke.

The fake smoke path remains deterministic and visibly fake. The real-provider
paths fail closed when no provider is configured and do not silently fall back
to fake translation.

## Ignored Artifact State

`git status --short --ignored` showed only ignored local outputs and caches:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- package `__pycache__/` directories
- `tests/__pycache__/`
- `tmp/`

No nonignored package output, screenshot, log, local app data, smoke data, OCR
cache, certificate, private key, signed binary, timestamp response, keyring
export, `.env` file, provider secret, or tester personal data was staged or
committed by the base package validation.

## Round 5 Self-Checks

Debug self-check:

- The base package result covers dry-run, build, source fake, packaged fake,
  source real-provider expected rejection, packaged real-provider expected
  rejection, base credential-smoke expected rejection, and ignored artifact
  state.
- Success, expected rejection, fake label, missing provider, keyring-free,
  no-artifact, and no-secret states are covered.

Architecture self-check:

- The base lane remains deterministic and keyring-free.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- No credential support is silently added to the base package.
- No signing, certificate, installer, updater, release feed, public release,
  cloud, OAuth, browser extension, AI summary, global hotkey, provider rewrite,
  OCR/capture rewrite, full localization, signed artifact, timestamp response,
  or signing log is introduced.
