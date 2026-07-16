# P22 Unsigned Private Trial Release Notes

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: baseline revalidated; tester instructions refresh in progress

These notes are for continuing controlled SnapLex private-trial validation
while signing remains paused. P22 is not a public release, signing rehearsal,
installer, updater, release feed, or runtime feature phase.

## Trust Label

Current trust label: `unsigned-private-trial`.

All P22 trial artifacts are unsigned private-trial artifacts. Signing remains
PAUSED until a later planner-approved signing phase receives every input listed
in `docs/p21_signing_unblock_requirements.md`.

Do not run signing commands in P22. Do not create, import, purchase, invent, or
use certificates. Do not call timestamp services. Do not produce signed
binaries or signed archives.

## Accepted Baseline Revalidated

P21 remains the accepted baseline for P22:

- accepted P21 commit:
  `96b193e9c6dfbdae3f89c59d4bea76c500846a30`;
- planner P22 guide commit:
  `b85bda0918da4d6fc6e30ce239871f95b6e1eb8d`;
- current P22 dispatch HEAD:
  `38655382adb59b08e37ca251947d0800cd93e88c`;
- `main` is aligned with `origin/main`;
- P21 recorded signing state as PAUSED because no explicit safe
  throwaway/test signing path approval was supplied after P20;
- P21 did not run signing commands, create/import/purchase/invent/use
  certificates, call timestamp services, create signed artifacts, or approve
  public release;
- `base` remains the deterministic, keyring-free package lane;
- `credentials` remains explicit and private-trial only.

Round 1 revalidation results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed.
- `python scripts\package_windows.py --dry-run --variant credentials` passed.

## Local Ignored Artifact State

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

No nonignored package output, signing material, certificate, private key,
signed binary, timestamp response, screenshot, log, `.env`, keyring export,
tester data, local app data, smoke data, OCR cache, or provider secret was
present at the start of P22 editing.

## P22 Continuity Position

P22 continues private-trial operations only when these boundaries hold:

- fake smoke mode remains deterministic and visibly fake;
- real-provider paths fail closed when no real provider is configured;
- provider secrets stay out of docs, logs, screenshots, tests, package
  resources, config/history files, and git;
- package outputs and smoke data remain ignored local artifacts;
- tester feedback must use synthetic or non-sensitive text;
- screenshots and logs are not accepted when they contain sensitive content;
- `base` and `credentials` package lanes remain separate.

Round 2 will expand these notes into current tester-facing instructions and
trust-label language.

## Round 1 Self-Checks

Debug self-check:

- The result is explained by the smallest P22 starting workflow: accept P21,
  confirm current HEAD, confirm deterministic validation, confirm package
  dry-runs, and record that signing remains PAUSED.
- Success, expected rejection, missing real provider, paused signing, ignored
  local output, no-certificate, no-signing-command, no-artifact, and no-secret
  states are covered.

Architecture self-check:

- Rebaseline work does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, release feed,
  cloud, OAuth, browser extension, AI summary, global hotkey, provider rewrite,
  OCR/capture rewrite, full localization, certificate, private key, signed
  artifact, timestamp response, or signing log is introduced.
