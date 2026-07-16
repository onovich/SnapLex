# P19 To P20 Handoff

Date: 2026-07-17
Status: P19 executor-complete; ready for planner check

Recommended P20: approved signing path acquisition and isolated signing
rehearsal setup gate.

P20 guide: to be created by planner after P19 acceptance.

## P19 Outcome

P19 passes as a signing rehearsal and signed archive candidate gate without
creating signed artifacts.

Decision summary:

- Signing path decision: SKIPPED because no approved safe throwaway/test signing
  path was supplied.
- Signing rehearsal: SKIPPED; no signing commands were run.
- Signature verification: NOT RUN because no signed artifact exists.
- Signed archive candidate: NOT READY for production, transfer, public release,
  installer, updater, or release feed.
- `base` remains deterministic and keyring-free.
- `credentials` remains explicit, private-trial, and validated with
  runtime-generated throwaway fake credential values.
- No certificate, private key, signed binary, timestamp response, signing log,
  screenshot, package output, `.env`, keyring export, local app data, smoke data,
  tester personal data, OCR cache, provider secret, or public release artifact
  was committed.

## P19 Deliverables

- `docs/p19_signing_path_decision.md`
- `docs/p19_base_package_control_evidence.md`
- `docs/p19_credentials_package_candidate_evidence.md`
- `docs/p19_signing_rehearsal_evidence.md`
- `docs/p19_signature_verification_policy.md`
- `docs/p19_signed_archive_stop_conditions.md`
- `docs/p19_signed_archive_candidate_decision.md`
- `docs/p19_boundary_scan_evidence.md`
- `docs/p19_validation_precheck_evidence.md`
- `docs/p19_final_validation_report.md`
- `docs/p19_to_p20_handoff.md`

## Validation To Preserve

- `Validate.cmd` PASS with 264 tests.
- `git diff --check` PASS.
- Version and no-GUI bootstrap PASS.
- Real-provider readiness rejects missing real provider setup.
- Base and credentials package dry-runs PASS.
- Base package build PASS through `SmokeTrial.cmd`.
- `SmokeTrial.cmd` PASS.
- `StartTrial.cmd --no-gui` expected rejection PASS.
- `StartFakeTrial.cmd --no-gui` PASS.
- `StartPackagedFakeTrial.cmd --no-gui` PASS.
- `StartPackagedTrial.cmd --no-gui` expected rejection PASS.
- Base package credential smoke expected rejection PASS.
- Credentials package build PASS.
- Credentials package import/cycle/save/check-delete PASS.
- P9 and P11 GUI smoke PASS with screenshots under ignored smoke data.
- P19 docs link/index PASS.
- Artifact, secret, private-key, certificate, package-output, screenshot, and
  signing-material scans PASS.

## Boundaries To Preserve

- Do not commit certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env` files, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
- Do not require, purchase, import, invent, or use production certificates
  unless separately approved.
- Do not run signing commands without an approved safe throwaway/test signing
  path and local-only evidence plan.
- Do not silently add keyring support to the base package.
- Keep the credential-capable package explicit and private-trial unless a later
  release gate approves otherwise.
- Keep providers behind provider registry and `TranslationPipeline`.
- Keep credentials behind credential services/stores, settings, provider setup,
  and trial readiness.
- Optional real-provider smoke still requires existing local credentials and
  explicit human network approval.
- Do not implement SnapLex Cloud, OAuth, billing, token broker, browser
  extension runtime, AI summary runtime, global hotkeys, broad provider/OCR/
  capture rewrites, full localization, installer runtime, updater runtime,
  release feed, or public release without a later approval gate.

## Known Limitations For P20

- No approved safe throwaway/test signing path exists.
- No production signing identity, certificate custody execution path, or
  production certificate exists.
- No signed artifact verification, timestamp, trust prompt, or revocation
  evidence exists.
- No signed archive candidate is approved for production or transfer.
- No installer, updater, release feed, public support channel, or public release
  path exists.
- No external P19 tester feedback was supplied.
- No real-provider network smoke was run.
- Locked Credential Locker, enterprise-managed keyring policy, unsupported
  backend, remote-session behavior, and broader tester device matrix evidence
  remain limited.

## Recommended P20 Scope

P20 should decide whether a safe throwaway/test signing path is approved.

Suggested P20 work if a safe signing path is supplied:

- document signing identity, certificate source, custody, and local-only
  artifact path before running commands;
- run signing rehearsal only in ignored local artifact paths;
- verify hash, Authenticode signature, timestamp, and trust status;
- record evidence without certificates, private keys, signed binaries,
  timestamp responses, logs, screenshots, or secrets;
- preserve deterministic base package and explicit credentials package smoke;
- stop immediately on signing, timestamping, verification, trust, cleanup, or
  boundary scan failure.

Suggested P20 work if no safe signing path is supplied:

- keep signing SKIPPED/BLOCKED;
- keep signed archive candidate work blocked;
- preserve private-trial archive handling without producing signed artifacts.

Recommended P20 non-scope:

- public release;
- production certificate purchase, import, custody execution, or use unless
  separately approved;
- committed signing material or signed artifacts;
- installer/updater runtime or release feed;
- SnapLex Cloud, account OAuth, billing, token broker, browser extension, AI
  summary, global hotkeys, broad provider/OCR/capture rewrites, or full
  localization.
