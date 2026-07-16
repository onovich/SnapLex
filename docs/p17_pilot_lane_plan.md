# P17 Limited Credential Package Pilot Lane Plan

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: controlled private tester lane defined

P17 starts from the planner-accepted P16 baseline and keeps the explicit
`credentials` package candidate inside a small, privacy-safe private tester
lane. This is not a public release, signed installer, updater, or default/base
package change.

## Baseline Revalidation

Source commit at P17 start:
`4394ff6648871e07b2be4dae9ad188b8a1a1af53`.

Round 1 rebaseline commands:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with 264 tests.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: expected rejection PASS with
  `Real translation provider is not configured.`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.

No package artifact was produced in this round. Dry-runs confirm the base and
credentials lanes are still explicit and available.

## Pilot Lane Objective

The P17 pilot lane validates whether the P16-approved unsigned
`credentials` package candidate can be shared with a controlled private tester
group without weakening the deterministic base package or leaking secrets.

The lane answers these decisions:

- whether credentials remain a separate package variant;
- whether signing is required before broader distribution;
- whether an installer or updater is required before a wider trial;
- how package artifacts are transferred, retained, and retired;
- how support escalates keyring, cleanup, and real-provider blockers.

## Allowed Pilot Participants

Allowed participants:

- one to three trusted private testers or maintainer-controlled Windows test
  machines;
- testers who can follow no-secret feedback rules;
- testers who understand the artifact is unsigned and private-trial only;
- testers who can run command-line smoke steps and report status lines.

Not allowed in this lane:

- public download links;
- anonymous or broad external distribution;
- testers asked to share provider keys, `.env` files, keyring exports,
  screenshots of credential fields, provider dashboards, private documents,
  logs with secrets, or personal data.

## Package Lanes

| Lane | Variant | P17 purpose | Required result |
| --- | --- | --- | --- |
| Base control lane | `base` | Preserve deterministic fake package behavior and prove keyring stays excluded. | Fake package smoke passes; credential smoke rejects keyring as unavailable. |
| Credential pilot lane | `credentials` | Validate explicit keyring-capable package candidate for controlled private testers. | Import/cycle/save/check-delete smoke passes or records a precise blocker. |

The `base` package remains the default deterministic path. The
`credentials` package is selected only by explicit package build and pilot
instructions.

## Pre-Share Gate Summary

Before sharing any credential candidate artifact, P17 requires:

- clean source commit recorded;
- source validation gate passing;
- base package control lane passing;
- credential candidate lane passing or blocker accepted for that tester lane;
- cleanup status recorded as `missing` after credential smoke;
- artifact label recorded with source commit, variant, date, and unsigned
  private-trial status;
- tester setup, cleanup, keyring failure, and no-secret feedback rules linked;
- artifact and secret scans passing.

If a gate fails, the credential package is not shared. The deterministic base
package may still be used for fake smoke.

## Tester Feedback Envelope

Tester feedback may include:

- package variant;
- source commit or artifact label;
- smoke command status lines;
- keyring backend class label;
- whether cleanup ended as `missing`;
- provider readiness category when real-provider testing is explicitly
  approved.

Tester feedback must not include:

- provider API keys, bearer tokens, or `.env` contents;
- keyring exports;
- smoke credential values;
- screenshots of credential fields or provider dashboards;
- private documents or translated private text;
- package logs or API responses containing sensitive data.

## Real-Provider Network Rule

Automated validation remains no-network. Optional real-provider smoke is
skipped unless all of these are true in the executor session:

- local credentials already exist;
- a human explicitly approves network use;
- outputs omit credential values and private translated content;
- pass/fail/blocker evidence can be recorded without secrets.

Round 1 has no such approval and no real-provider network smoke was run.

## Round 1 Self-Checks

Debug self-check:

- The current result is explained by the smallest pilot workflow: accepted P16
  baseline, source validation, base/credentials dry-run lanes, and real-provider
  fail-closed readiness.
- PASS, expected rejection, no-network, no tester feedback yet, and no-secret
  states are represented.

Architecture self-check:

- The credential-capable path remains explicit as the `credentials` package
  variant.
- The base package remains deterministic and keyring-free.
- Credential behavior remains behind `CredentialService` and credential stores.
- Provider execution remains behind provider registry and `TranslationPipeline`.
- No cloud, OAuth, billing, token broker, browser extension, AI summary,
  global hotkey, OCR/capture rewrite, full localization, package artifact, or
  secret enters P17.
