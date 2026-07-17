# P23 Next Action Register

Date: 2026-07-17
Phase: P23 Private Trial Feedback Intake And Support Loop Gate
Status: internal continuity actions registered

P23 has no external tester feedback to repair. This register tracks the
remaining support-loop actions required before the phase can return to the
planner for review.

## Action Register

| ID | Source | Action | Owner | Status | Exit condition |
| --- | --- | --- | --- | --- | --- |
| P23-A01 | P23 guide | Revalidate deterministic base package lane. | executor | done | Base dry-run, source/package fake smoke, real-provider expected rejections, and base credential-smoke expected rejection are recorded in `docs/p23_base_package_continuity_evidence.md`. |
| P23-A02 | P23 guide | Revalidate explicit credentials package lane. | executor | open | Credentials dry-run/build and import/cycle/save/check-delete smoke pass with throwaway generated values, then base package behavior is restored. |
| P23-A03 | P23 guide | Record artifact retention and support-loop evidence. | executor | open | P23 documents that no external artifacts were accepted and generated local outputs remain ignored. |
| P23-A04 | P23 guide | Run boundary, secret, certificate, private-key, package-output, screenshot, log, and signing-material scans. | executor | open | Scans are recorded with no forbidden nonignored artifacts or raw secrets. |
| P23-A05 | P23 guide | Write final validation report and P24 handoff. | executor | open | Final report and handoff include validation evidence, known limitations, and next recommendation. |
| P23-A06 | P23 guide | Notify planner thread with READY_FOR_CHECK after final commit and push. | executor | open | Planner thread receives final commit, report paths, validation evidence, boundaries, limitations, and recommendation. |
| P23-A07 | Future support loop | Route any late external feedback to the next privacy-safe intake. | planner/support | monitoring | Feedback is screened before storage and never includes secrets or sensitive artifacts. |

## Deferred Or Rejected Actions

| ID | Action | Disposition | Reason |
| --- | --- | --- | --- |
| P23-D01 | Run signing commands or create/import/use certificates. | rejected for P23 | Signing remains PAUSED and P23 is not a signing phase. |
| P23-D02 | Produce signed archive, installer, updater, release feed, or public release. | rejected for P23 | Out of scope for the non-signing private-trial support loop. |
| P23-D03 | Add keyring support silently to the base package. | rejected for P23 | Base package must remain deterministic and keyring-free. |
| P23-D04 | Run real-provider network smoke without local credentials and explicit approval. | rejected for P23 | No approved credentials or human network approval were supplied. |
| P23-D05 | Implement SnapLex Cloud, OAuth, billing, token broker, browser extension, AI summary, global hotkeys, broad provider/OCR/capture rewrites, or full localization. | rejected for P23 | Broad feature expansion is outside the phase boundary. |

## Round 4 Self-Checks

Debug self-check:

- The register translates the no-feedback decision into concrete remaining
  evidence work rather than inventing tester issues.
- Open, monitoring, deferred, rejected, no-network, no-signing, no-artifact, and
  no-secret states are covered.

Architecture self-check:

- Actions preserve the accepted provider, credential, settings, history,
  capture, OCR, package, and trial readiness boundaries.
- Any future support input must be privacy-screened before repository evidence
  is written.
- No runtime feature, signing path, installer, updater, release feed, or public
  release behavior is introduced.
