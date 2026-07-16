# P19 Signing Path Decision

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: round 1 baseline recorded; signing path decision pending round 2

P19 decides whether SnapLex has an approved safe throwaway/test signing path
for an isolated signing rehearsal. Round 1 revalidates the accepted P18
baseline and records the decision inputs. It does not run signing tools, create
certificates, import signing material, or generate signed artifacts.

## Accepted Baseline Revalidated

P18 remains the accepted baseline for P19:

- accepted P18 commit:
  `9055bd7c565b3965b22bb267aebdd5ae7f8b1aa6`;
- planner P19 guide commit:
  `f3f36d168d1839fa5e59c804a02d42459f697c7d`;
- current P19 dispatch commit:
  `e3166ea49f96ffd6e5341a4426ff73593126f413`;
- `main` is aligned with `origin/main`;
- `base` remains the deterministic, keyring-free package lane;
- `credentials` remains explicit and private-trial only;
- P18 recorded signing rehearsal as SKIPPED because no approved safe
  throwaway/test signing path was supplied;
- P18 did not approve public release, production signing, installer runtime,
  updater runtime, silent keyring in base, cloud accounts, browser extension
  runtime, AI summary runtime, global hotkeys, broad provider/OCR/capture
  rewrites, or full localization.

Round 1 revalidation results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed.
- `python scripts\package_windows.py --dry-run --variant credentials` passed.

The first credentials dry-run attempt in a parallel command group hit a
sandbox process ACL error before project execution. The same command passed
when rerun directly, so P19 records the project result as PASS.

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
present at the start of P19 editing.

## Signing Approval Inputs

Round 2 must decide whether P19 has an approved safe throwaway/test signing
path. Required inputs for an approved run are:

- explicit approval to use a throwaway/test signing path;
- confirmation that no production certificate is being used;
- ignored local artifact path for any rehearsal output;
- no certificate/private-key material committed or copied into tracked files;
- verification evidence recorded as text without binaries, screenshots,
  timestamp response bodies, logs, secrets, token PINs, or passwords;
- cleanup and boundary scans after any rehearsal.

Current round 1 evidence does not include approval for a signing path.

## Round 1 Self-Checks

Debug self-check:

- The result is explained by the smallest P19 starting workflow: accept P18,
  confirm HEAD, confirm deterministic validation, confirm package dry-runs,
  and list signing approval inputs.
- Success, expected rejection, ignored local output, no certificate, no signing
  path, skipped network, and no-secret states are covered.

Architecture self-check:

- Rebaseline work does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, or signed artifact is
  introduced.
