# P18 To P19 Handoff

Date: 2026-07-17
Status: P18 planner-accepted; ready for P19 execution

Recommended P19: signing rehearsal and signed archive candidate gate.

P19 guide:
`docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`

P19 TODO: `docs/p19_todo.md`

## P18 Outcome

P18 passes as a signing and distribution readiness gate.

The phase records signing identity, certificate custody, verification,
rehearsal, archive-versus-installer, rollback/update, artifact retention,
revocation, support escalation, and distribution readiness decisions.

Decision summary:

- `base` remains deterministic and keyring-free.
- `credentials` remains explicit and private-trial.
- Archive lane remains the only currently eligible private-trial format.
- Installer, updater, public release, and production signing are not approved.
- Signing rehearsal is SKIPPED because no approved safe throwaway/test signing
  path was supplied.
- P19 may consider a safe isolated signing rehearsal or signed archive
  candidate gate.

## P18 Deliverables

- `docs/p18_signing_identity_certificate_custody.md`
- `docs/p18_signing_verification_policy.md`
- `docs/p18_signing_rehearsal_record.md`
- `docs/p18_archive_installer_readiness_decision.md`
- `docs/p18_rollback_update_policy.md`
- `docs/p18_artifact_retention_revocation_support.md`
- `docs/p18_distribution_readiness_decision.md`
- `docs/p18_boundary_scan_evidence.md`
- `docs/p18_package_validation_evidence.md`
- `docs/p18_final_validation_report.md`
- `docs/p18_to_p19_handoff.md`

## Validation To Preserve

- `Validate.cmd` PASS with 264 tests.
- `git diff --check` PASS.
- Version and no-GUI bootstrap PASS.
- Real-provider readiness rejects missing real provider setup.
- Base and credentials package dry-runs PASS.
- Base package build PASS.
- `SmokeTrial.cmd` PASS.
- `StartTrial.cmd --no-gui` expected rejection PASS.
- `StartFakeTrial.cmd --no-gui` PASS.
- `StartPackagedFakeTrial.cmd --no-gui` PASS.
- `StartPackagedTrial.cmd --no-gui` expected rejection PASS.
- Base package credential smoke expected rejection PASS.
- Credentials package build PASS.
- Credentials package import/cycle/save/check-delete PASS.
- Final base package restore PASS.
- Restored base package credential smoke expected rejection PASS.
- P9 and P11 GUI smoke PASS with screenshots under ignored smoke data.
- P18 docs link/index PASS.
- Artifact, secret, private-key, and signing-material scans PASS.

## Boundaries To Preserve

- Do not commit certificates, private keys, signed binaries, package outputs,
  screenshots, logs, `.env` files, keyring exports, tester personal data, local
  app data, smoke data, OCR caches, or provider secrets.
- Do not silently add keyring support to the base package.
- Keep the credential-capable package explicit and private-trial unless a later
  gate approves otherwise.
- Keep providers behind provider registry and `TranslationPipeline`.
- Keep credentials behind credential services/stores, settings, provider setup,
  and trial readiness.
- Optional real-provider smoke still requires existing local credentials and
  explicit human network approval.
- Do not implement SnapLex Cloud, OAuth, billing, token broker, browser
  extension runtime, AI summary runtime, global hotkeys, broad provider/OCR/
  capture rewrites, full localization, installer runtime, updater runtime, or
  public release without a later approval gate.

## Known Limitations For P19

- No production signing identity or certificate custody execution path exists.
- No safe throwaway/test signing path was supplied in P18.
- No signed artifact verification evidence exists.
- No installer, updater, release feed, public support channel, or public
  release path exists.
- No external P18 tester feedback was supplied.
- No real-provider network smoke was run.
- Locked Credential Locker, enterprise-managed keyring policy, unsupported
  backend, remote-session behavior, and broader tester device matrix evidence
  remain limited.

## Recommended P19 Scope

P19 should decide whether to run an isolated signing rehearsal or signed archive
candidate gate.

Suggested P19 work:

- approve or explicitly skip a safe throwaway/test signing path;
- run signing rehearsal only in ignored local artifact paths;
- record signing and verification evidence without secrets or binaries;
- keep archive lane private-trial unless later release criteria pass;
- preserve deterministic base package and explicit credentials package smoke;
- define stop conditions if signing, timestamping, verification, trust prompt,
  or credential cleanup fails.

Recommended P19 non-scope:

- public release;
- production certificate purchase or use unless separately approved;
- committed signing material or signed artifacts;
- installer/updater runtime;
- SnapLex Cloud, account OAuth, billing, token broker, browser extension, AI
  summary, global hotkeys, broad provider/OCR/capture rewrites, or full
  localization.
