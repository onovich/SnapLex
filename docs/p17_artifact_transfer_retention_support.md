# P17 Artifact Transfer, Retention, And Support Policy

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: private-trial artifact policy ready

This policy applies only to the controlled P17 private tester lane for the
explicit unsigned `credentials` package candidate. It does not authorize public
release, a signed installer, updater, base-package keyring support, cloud
accounts, OAuth, billing, token broker, browser extension runtime, AI summary
runtime, global hotkeys, provider rewrites, OCR/capture rewrites, or full
localization.

## Artifact Eligibility

An artifact is eligible for P17 private transfer only when:

- `docs/p17_package_candidate_gate_evidence.md` records a passing source gate;
- the base control lane passed and remains keyring-free;
- the credential candidate lane passed or has a precise accepted blocker for
  that tester lane;
- credential smoke cleanup ended as PASS or `missing`;
- artifact and secret scans pass before transfer;
- the artifact is labeled unsigned/private-trial only;
- tester setup, cleanup, failure-mode, and no-secret feedback rules are sent
  with the artifact.

If any of these checks fail, do not transfer the credential candidate.

## Allowed Transfer Lane

Allowed:

- private transfer to one to three trusted testers or maintainer-owned Windows
  test machines;
- transfer of the selected local `dist\SnapLex` folder or an archive created
  outside git;
- artifact label containing:
  - `SnapLex`;
  - source commit prefix;
  - `credentials`;
  - date;
  - `unsigned-private-trial`;
- out-of-band confirmation that the tester received the intended label.

Not allowed:

- public download links;
- attaching artifacts to repository commits;
- committing `build\`, `dist\`, installers, archives, screenshots, local app
  data, smoke data, logs, OCR caches, keyring exports, `.env`, provider secrets,
  tester personal data, or package binaries;
- transfer that asks testers to weaken Windows security policy or export
  Credential Locker data.

## Retention Policy

Recommended retention:

- keep each P17 credential candidate artifact only until the pilot lane is
  accepted, rejected, or superseded;
- retire artifacts immediately after a blocker requires a rebuild;
- keep only privacy-safe evidence in docs, such as command names, status lines,
  backend labels, artifact labels, source commit, and cleanup status;
- remove local `build\`, `dist\`, and `snaplex-smoke-data\` after final P17
  validation if no further package smoke is needed.

Do not preserve:

- raw package logs containing local paths beyond what is already summarized;
- real provider responses;
- `.env` files;
- keyring exports;
- screenshots containing credential fields or private translated text;
- tester personal data.

## Support Escalation

Escalate as `S0 Blocker` when:

- package launch or no-gui bootstrap fails for the selected artifact;
- credential smoke output exposes a raw secret or asks for one in feedback;
- cleanup cannot be verified after `save`;
- real-provider mode runs without explicit approval;
- the base package unexpectedly includes keyring support.

Escalate as `S1 Critical` when:

- `credentials` import cannot discover a backend on a selected tester lane;
- cycle smoke cannot save/read/delete;
- save/check-delete restart readiness fails;
- enterprise policy or locked Credential Locker blocks all credential smoke on
  a selected tester machine.

Escalate as `S2 Major` when:

- setup instructions are confusing but the tester can continue safely;
- artifact label or transfer path is ambiguous;
- cleanup requires a manual retry but ends safely as missing.

Defer or reject reports when:

- they ask for public release, signed installer, updater, cloud accounts,
  OAuth, billing, hosted token broker, browser extension runtime, AI summary,
  global hotkeys, full localization, broad provider rewrites, or OCR/capture
  rewrites;
- they include secrets or personal data and need safe resubmission.

## Cleanup Expectations

Maintainer cleanup:

- verify the packaged smoke credential status returns to `missing`;
- keep generated package outputs and smoke data out of git;
- remove local generated folders when they are no longer needed.

Tester cleanup:

- run `SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete`
  when asked to clean a retained smoke credential;
- delete the local trial package folder after the pilot lane closes;
- do not export Credential Locker data.

## Round 6 Self-Checks

Debug self-check:

- The policy covers transfer, artifact labels, retention, cleanup, support
  escalation, expected rejection, unavailable backend, skipped network, and
  no-secret states.
- The current result can be explained by the smallest private package
  workflow: eligible artifact, controlled transfer, finite retention, and
  escalation categories.

Architecture self-check:

- Artifact policy does not change package scripts, provider behavior,
  credential services, settings, UI, OCR, or capture code.
- The credential package remains an explicit private-trial variant.
- The base package remains deterministic and keyring-free.
- Generated outputs, screenshots, package outputs, local app data, smoke data,
  keyring exports, logs, `.env`, tester personal data, and provider secrets
  remain outside git.
