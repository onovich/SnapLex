# P19 TODO

Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate

Guide: `docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`

Status: ready for executor

Round budget: 12 conversation rounds

## Tasks

- [x] Rebaseline P18 signing/distribution reports and current package lanes.
- [ ] Decide whether an approved safe throwaway/test signing rehearsal path
  exists.
- [ ] Revalidate deterministic base package behavior.
- [ ] Revalidate explicit credentials package behavior.
- [ ] Run approved local signing rehearsal, or record SKIPPED/BLOCKED with a
  precise reason.
- [ ] Record signature verification, trust, timestamp, and evidence policy.
- [ ] Define signed archive stop conditions, cleanup, rollback, and support
  implications.
- [ ] Decide whether signed archive candidate work may proceed to a later gate.
- [ ] Run artifact, secret, private-key, certificate, and signing-material scans.
- [ ] Write final validation report and P20 handoff.
- [ ] Commit and push.

## Deferred

- Public release.
- Production certificate purchase, import, custody execution, or use unless
  explicitly approved outside this goal.
- Committed certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env`, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
- Installer runtime, updater runtime, release feed, and auto-update behavior.
- Silent keyring support in the base package.
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension runtime,
  AI summary runtime, global hotkeys, broad provider/OCR/capture rewrites, or
  full localization.
- Real-provider network smoke without existing local credentials and explicit
  human approval.
