# P22 Artifact Transfer, Retention, Cleanup, And Support Policy

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: unsigned private-trial artifact policy refreshed

This policy applies to P22 unsigned private-trial source, base package, and
explicit credentials package lanes. It does not authorize signing, signed
archives, installers, updaters, release feeds, public download pages, or public
release.

## Artifact Eligibility

An artifact or source handoff is eligible for P22 private-trial transfer only
when:

- source validation is green for the current commit;
- signing state is still PAUSED and the trust label is
  `unsigned-private-trial`;
- `docs/p22_unsigned_private_trial_release_notes.md` is sent with the handoff;
- `docs/p22_tester_support_intake.md` and
  `docs/p22_feedback_triage_criteria.md` define the support and feedback path;
- the `base` lane has passed fake smoke, fail-closed real-provider checks, and
  keyring-free credential-smoke rejection;
- the `credentials` lane, when shared, has passed import/cycle/save/check-delete
  with runtime-generated throwaway values;
- final transfer uses only ignored local or private out-of-band artifact paths;
- boundary scans confirm package outputs, screenshots, logs, local app data,
  smoke data, OCR caches, `.env` files, keyring exports, certificates, private
  keys, signed binaries, timestamp responses, tester data, and provider secrets
  are not committed.

If any condition fails, do not transfer the affected artifact.

## Artifact Label

Use this label shape for any P22 private-trial artifact:

```text
SnapLex-0.1.0-<commit-prefix>-<lane>-<yyyymmdd>-unsigned-private-trial
```

Allowed `lane` values:

- `source`
- `base`
- `credentials`

Label rules:

- `credentials` must be visible when keyring support is included.
- `base` must not include keyring support.
- `unsigned-private-trial` must remain visible on every P22 transfer.
- Do not use `signed`, `test-signed`, `installer`, `updater`, `public`,
  `release`, or similar wording for P22 artifacts.

## Allowed Transfer Lane

Allowed:

- direct controlled handoff to trusted private testers or maintainer-owned
  Windows test machines;
- an access-controlled private link with limited access and a clear expiry;
- transfer of a local `dist\SnapLex` folder or archive created outside git;
- transfer of source checkout instructions that point to a pushed commit;
- non-secret manifest information: artifact label, source commit, lane,
  unsigned/private-trial status, optional SHA256 hash, validation summary, and
  support/cleanup instructions.

Not allowed:

- public download links, unauthenticated mirrors, package registries, app stores,
  release feeds, or updater endpoints;
- attaching artifacts to repository commits, issues, docs, or pull requests;
- committing `build\`, `dist\`, package archives, installers, screenshots,
  local app data, smoke data, logs, OCR caches, keyring exports, `.env` files,
  tester personal data, certificates, private keys, signed binaries, timestamp
  responses, or provider secrets;
- transfer instructions that ask testers to weaken Windows security policy,
  export Credential Locker data, paste API keys into feedback, or share private
  documents.

## Retention Policy

Retain in git:

- source code;
- Markdown release notes, support policy, triage criteria, validation evidence,
  boundary scans, final report, and handoff;
- non-secret artifact metadata such as label, source commit, lane, command name,
  status, and cleanup result.

Do not retain in git:

- package binaries or archives;
- raw package logs, screenshots, generated app data, smoke data, OCR caches,
  `.env` files, keyring exports, provider responses, tester personal data,
  certificates, private keys, signed binaries, timestamp responses, or provider
  secrets.

Recommended private artifact retention:

- expire or delete an unsigned private-trial artifact within 14 days after the
  tester window closes;
- disable transfer access immediately when an artifact is superseded,
  withdrawn, or fails a safety check;
- keep only non-secret manifest evidence after the support window ends;
- remove local `build\`, `dist\`, `snaplex-smoke-data\`, and `tmp\` folders
  when no further package smoke is needed.

## Cleanup Expectations

Maintainer cleanup:

- if a credentials package `save` smoke was run, follow with
  `check-delete` and record the cleanup result;
- rebuild `base` after credentials package validation when the local package
  state should return to deterministic base;
- verify `git status --short --ignored` shows generated outputs only as ignored
  local artifacts;
- do not stage generated outputs, screenshots, logs, local app data, smoke data,
  OCR caches, keyring exports, `.env`, tester data, certificates, private keys,
  signed binaries, timestamp responses, or provider secrets.

Tester cleanup:

- delete the local trial package folder after the pilot lane closes;
- run `SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete`
  when asked to clean a retained smoke credential;
- do not export Credential Locker data;
- do not redistribute private-trial artifacts.

## Withdrawal And Revocation

Withdraw an artifact when:

- artifact label, lane, source commit, or hash does not match the recorded
  evidence;
- the base package includes keyring support or credential-only dependencies;
- the credentials package fails cleanup without a safe environment explanation;
- real-provider behavior silently falls back to fake while appearing real;
- tester feedback or support intake reveals a secret/privacy leak risk;
- Windows trust prompt reports suggest testers believe the artifact is signed,
  public, or production-approved;
- any package output, screenshot, log, local app data, smoke data, OCR cache,
  `.env`, keyring export, certificate, private key, signed binary, timestamp
  response, tester data, or provider secret is accidentally committed.

Withdrawal actions:

- disable private transfer access;
- notify affected testers not to run or redistribute the candidate;
- keep only non-secret metadata in docs;
- rotate or revoke any affected provider credential outside git when exposure
  is suspected;
- fall back to the last accepted deterministic base lane or a newly validated
  replacement.

## Support Escalation

Escalate as `S0 Blocker` when:

- a transfer or support path risks exposing secrets, personal data, private
  documents, certificates, private keys, signed artifacts, or package outputs;
- base package keyring-free behavior regresses;
- credentials package smoke prints a raw credential value or cannot clean up
  after `save`;
- artifact wording suggests signed/public release status;
- generated outputs are staged or committed.

Escalate as `S1 Critical` when:

- package launch, no-GUI bootstrap, fake smoke, or packaged fake smoke fails;
- real-provider paths do not fail closed when missing configuration;
- credentials import/cycle/save/check-delete fails on a selected private tester
  lane;
- trust-prompt friction blocks the selected tester lane with no documented
  workaround.

Classify as `S2 Major` when setup, artifact label, transfer path, trust prompt,
DPI, multi-monitor, assistive-technology, or Credential Locker behavior is
confusing but the tester can continue safely.

Reject or request resubmission when a report includes sensitive material or
asks P22 to expand into signing, installer, updater, release feed, public
release, cloud, account OAuth, billing, hosted token broker, browser extension
runtime, AI summary runtime, global hotkeys, broad provider/OCR/capture
rewrites, or full localization.

## No-Secret Evidence Checklist

Before committing P22 artifact evidence, verify:

- command names and status lines are enough to explain the result;
- raw provider keys, `.env` contents, keyring exports, private documents,
  screenshots with sensitive content, logs, package binaries, local app data,
  smoke data, OCR caches, certificates, private keys, signed binaries, timestamp
  responses, tester personal data, and provider secrets are absent;
- any hash or artifact label points only to a private ignored artifact, not to a
  committed binary;
- signing remains PAUSED and no signing command was run.

## Round 7 Self-Checks

Debug self-check:

- The policy covers eligibility, labels, allowed transfer, retention, cleanup,
  withdrawal, escalation, expected rejection, ignored artifacts, and no-secret
  evidence.
- It distinguishes source, base, and credentials lanes while keeping the
  current trust label unsigned/private-trial.

Architecture self-check:

- Artifact handling does not move provider, credential, settings, history,
  capture, OCR, UI, or trial readiness rules into docs or scripts.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit and private-trial only.
- No signing, certificate, timestamp, signed archive, installer, updater,
  release feed, public release, cloud, OAuth, browser extension, AI summary,
  global hotkey, provider rewrite, OCR/capture rewrite, or full localization is
  introduced.
