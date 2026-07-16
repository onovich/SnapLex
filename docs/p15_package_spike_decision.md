# P15 Package Spike Decision

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: promote to later production hardening phase; not a release promise

P15 proves the isolated credential-capable package spike on this Windows
executor environment. The decision is to promote credential-capable packaging
to a later production hardening phase, while keeping the current base package
as the deterministic private-trial smoke path.

## Decision

Promote to a later production hardening phase.

Do not treat P15 as a production credential-capable package release. P15
establishes feasibility and evidence only. A future phase must harden support,
document tester-facing behavior, define release gates, and decide whether to
ship a credential-capable package variant.

## Evidence

| Evidence | Result | Impact |
| --- | --- | --- |
| Explicit spike boundary | PASS | `credentials` is a named variant and is not the default. |
| Base package preservation | PASS | Base dry-run, base build, fake packaged smoke, and real packaged fail-closed paths remain green. |
| Base credential exclusion | PASS | Base packaged `--smoke-credentials` fails with `keyring is not available in this runtime.` |
| Packaged keyring import/backend discovery | PASS | Credentials variant discovers `keyring.backends.Windows.WinVaultKeyring`. |
| Packaged save/read/delete | PASS | Credentials variant saves, reads, deletes, and cleans up a throwaway runtime-generated value. |
| Packaged restart readiness | PASS | One packaged process saves; a second packaged process checks readiness and deletes. |
| Cleanup guidance | PASS | Maintainer cleanup instructions cover keyring reference, package outputs, and smoke data. |
| Deterministic tests | PASS | Package and release smoke tests cover the explicit variant and no-secret CLI output. |

## Why Promote

Promotion is justified because P15 demonstrates the hard parts of the package
credential path:

- keyring import/backend discovery works from a packaged executable;
- the Windows backend is available as `keyring.backends.Windows.WinVaultKeyring`;
- save/read/delete/cleanup works through `CredentialService` and
  `KeyringCredentialStore`;
- restart readiness works across two packaged processes;
- the base package path remains deterministic and does not silently include
  keyring;
- real trial paths still fail closed when no real provider is configured.

## Why Not Ship Yet

P15 is not enough to ship a production credential-capable package because:

- tester-facing UX and release notes for a credential-capable package are not
  finalized;
- installer/updater behavior is not defined;
- long-running cleanup and recovery guidance is maintainer-oriented, not
  end-user polished;
- failure modes such as locked Windows Credential Locker, enterprise policy
  restrictions, missing pywin32 runtime pieces, and non-Windows backends need
  more release hardening;
- no real-provider network smoke was run in P15;
- P15 did not define a signed distributable, support policy, or rollout plan.

## Recommended Next Phase

Recommended P16: Credential-Capable Package Production Hardening.

Suggested P16 scope:

- keep the base package deterministic and unchanged;
- harden the explicit credential-capable package variant;
- add tester-facing package credential setup and cleanup docs;
- define expected failure messages for unavailable/locked keyring backends;
- decide whether `credentials` remains a separate package variant or becomes a
  clearly labeled trial package artifact;
- preserve no-network automated validation and no-secret repository hygiene;
- optionally run real-provider smoke only with existing local credentials and
  explicit human network approval.

## Non-Scope Preserved

P15 does not implement or approve:

- production SnapLex Cloud;
- account OAuth, billing, hosted token broker, remote accounts, or cloud sync;
- browser extension runtime;
- AI summary runtime;
- global hotkeys;
- provider rewrites unrelated to package credential evidence;
- OCR/capture rewrites;
- full localization;
- real network validation in automated tests.

## Round 8 Self-Checks

Debug self-check:

- The current decision is explained by package spike evidence.
- Promote, not-ship-yet, no-secret, base preservation, and fail-closed states
  are covered.
- Remaining production hardening gaps are explicit.

Architecture self-check:

- Providers remain behind provider contracts and `TranslationPipeline`.
- Credentials remain behind `CredentialService` and credential stores.
- Packaging remains an explicit variant path and does not own provider,
  credential, settings, history, OCR, capture, or UI business rules.
