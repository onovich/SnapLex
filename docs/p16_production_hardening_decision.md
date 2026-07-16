# P16 Production Hardening Decision

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: approve limited private tester credential package candidate; not public release

P16 hardening evidence supports a limited private tester distribution of the
explicit `credentials` package candidate under the P16 release gate. This is
not approval for a broad public release, silent base-package keyring support,
or a signed installer.

## Decision

Approve a limited private tester credential package candidate.

Conditions:

- distribute only the explicit `credentials` variant;
- keep the deterministic `base` package lane unchanged;
- label the credential artifact as unsigned and private-trial only;
- require the P16 release gate before sharing;
- use only runtime-generated throwaway values for credential package smoke;
- collect feedback using no-secret rules;
- skip real-provider network smoke unless local credentials already exist and
  a human explicitly approves network use in that session.

## Evidence

| Gate | Result | Evidence |
| --- | --- | --- |
| P15 baseline revalidation | PASS | `Validate.cmd`, version/no-gui, dry-runs, real-provider expected rejection, fake smoke, and `SmokeTrial.cmd` passed at P16 start. |
| Base package preservation | PASS | Base build, fake package smoke, packaged real-trial expected rejection, and base credential-smoke expected rejection passed. |
| Credentials variant dependency gate | PASS | Credentials build included keyring hidden imports and discovered WinVaultKeyring from the packaged executable. |
| Credential smoke hardening | PASS | Import, cycle, save, and check-delete passed from source and packaged runtime with phase-neutral reference. |
| Failure-mode hardening | PASS | Store and backend failures are wrapped without leaking backend details; support policy covers locked/unavailable/unsupported states. |
| Tester setup and cleanup | PASS | Tester guide documents setup, smoke, cleanup, legacy cleanup, and feedback no-secret rules. |
| Release gate and artifact policy | PASS | Source, base, credentials, evidence, artifact, signing, and real-provider network gates are explicit. |
| No-network automated validation | PASS | Automated tests remain deterministic; real-provider smoke remains manual/approved only. |

## Why Limited Distribution Is Allowed

Limited private tester distribution is justified because:

- the credential-capable path is explicit as `--variant credentials`;
- the base package remains deterministic and keyring-free;
- packaged WinVault keyring import works;
- packaged save/read/delete and restart readiness pass;
- smoke output uses non-secret phase-neutral identifiers;
- failure wrapping avoids traceback-style secret/detail leakage;
- tester setup, cleanup, and feedback rules are documented;
- release gates keep artifacts and evidence controlled.

## Why Public Release Is Not Approved

Public release is not approved because:

- P16 does not produce a signed installer or updater;
- P16 does not define broad support commitments;
- enterprise keyring policies and locked Credential Locker behavior are covered
  as policy/blockers, not fully exercised across a device matrix;
- no real-provider network smoke was run in this executor session;
- artifact transfer, retention, and support escalation need a real pilot loop;
- the credential package should remain separate until private-trial evidence
  confirms the package lane is understandable.

## Distribution Envelope

Allowed:

- one or more controlled private testers;
- explicit `credentials` package candidate;
- unsigned artifact labeled with source commit, lane, date, and private-trial
  status;
- package smoke evidence using throwaway values;
- feedback that includes status lines and backend labels only.

Not allowed:

- broad public download;
- default/base package keyring inclusion;
- provider secrets in feedback, docs, screenshots, commits, logs, or chat;
- keyring exports;
- weakening local machine security policy to force a pass;
- signed release claims.

## Required Pre-Share Checklist

Before sharing a credential candidate package:

- run the source gate from `docs/p16_release_gate_artifact_policy.md`;
- run the base lane gate;
- run the credential candidate gate;
- confirm cleanup status is `missing`;
- run artifact and secret scans;
- record source commit and artifact label;
- link tester setup and cleanup guide;
- link keyring failure modes and support policy.

## Recommended P17

Recommended next phase: P17 Limited Credential Package Pilot And Signing
Decision.

Suggested P17 scope:

- execute the limited private tester package lane with one or more testers;
- collect no-secret feedback using P16 setup/failure/cleanup rules;
- record real-provider smoke only when explicitly approved with existing local
  credentials;
- decide whether to keep the credential package as a separate variant;
- define signing/installer/updater requirements or defer them with evidence;
- preserve deterministic base package validation.

## Round 8 Self-Checks

Debug self-check:

- The decision is explained by the smallest gate evidence: base lane,
  credentials lane, smoke hardening, failure modes, tester docs, and release
  policy.
- PASS, expected rejection, limited approval, public release rejection,
  skipped network, cleanup, and no-secret states are represented.

Architecture self-check:

- The decision keeps credential-capable packaging explicit and separate from
  base.
- Providers stay behind provider registry and `TranslationPipeline`.
- Credentials stay behind `CredentialService` and stores.
- No cloud, OAuth, billing, token broker, browser extension, AI summary,
  global hotkey, OCR/capture rewrite, or full localization scope is approved.
