# P20 TODO

Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate

Guide: `docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md`

Status: ready for executor

Round budget: 12 conversation rounds

## Tasks

- [x] Rebaseline accepted P19 and current package lanes.
- [x] Decide whether explicit safe signing-path approval exists.
- [x] Record required approval inputs for any rehearsal.
- [x] Define ignored local artifact directories, cleanup, and evidence
  retention policy.
- [x] Define command discovery and signing rehearsal command shape.
- [x] Run approved local-only rehearsal, or record BLOCKED/SKIPPED without
  running signing commands.
- [x] Define signature verification, trust, timestamp, and revocation evidence
  handling.
- [ ] Revalidate deterministic base package lane.
- [ ] Revalidate explicit credentials package lane.
- [ ] Run boundary, secret, private-key, certificate, package-output,
  screenshot, log, and signing-material scans.
- [ ] Write final validation report and P21 handoff.
- [ ] Commit and push.

## Deferred

- Public release.
- Production signing and production certificate custody execution unless
  separately approved outside this phase.
- Committed certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env`, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
- Installer runtime, updater runtime, release feed, auto-update behavior, and
  public support channel.
- Silent keyring support in the base package.
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension runtime,
  AI summary runtime, global hotkeys, broad provider/OCR/capture rewrites, or
  full localization.
