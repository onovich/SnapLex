# P20 To P21 Handoff

Date: 2026-07-17
Status: P20 planner-accepted; ready for P21 execution

Recommended P21: signing path unblock decision or pause signing work.

P21 guide:
`docs/p21_signing_path_unblock_decision_pause_gate_goal_guide.md`

P21 TODO: `docs/p21_todo.md`

## P20 Outcome

P20 passes as an approved signing path acquisition and rehearsal setup gate
without running signing commands or creating signed artifacts.

Decision summary:

- Signing path approval: BLOCKED/SKIPPED because no explicit safe
  throwaway/test signing path approval was supplied.
- Signing rehearsal: BLOCKED/SKIPPED; no signing commands were run.
- Signature verification: NOT RUN because no signed artifact exists.
- `signtool.exe`: not discoverable on PATH.
- `Get-AuthenticodeSignature`, `Set-AuthenticodeSignature`, and `Get-FileHash`
  are available for future approved command shapes.
- Current trust label: `unsigned-private-trial`.
- `base` remains deterministic and keyring-free.
- `credentials` remains explicit, private-trial, and validated with
  runtime-generated throwaway fake credential values.
- No certificate, private key, signed binary, timestamp response, signing log,
  screenshot, package output, `.env`, keyring export, local app data, smoke
  data, tester personal data, OCR cache, provider secret, or public release
  artifact was committed.

## P20 Deliverables

- `docs/p20_signing_path_approval_record.md`
- `docs/p20_rehearsal_artifact_directory_policy.md`
- `docs/p20_signing_command_discovery.md`
- `docs/p20_isolated_rehearsal_evidence.md`
- `docs/p20_signature_verification_evidence_policy.md`
- `docs/p20_base_package_control_evidence.md`
- `docs/p20_credentials_package_control_evidence.md`
- `docs/p20_boundary_scan_evidence.md`
- `docs/p20_validation_precheck_evidence.md`
- `docs/p20_final_validation_report.md`
- `docs/p20_to_p21_handoff.md`

## Validation To Preserve

- `Validate.cmd` PASS with 264 tests.
- `git diff --check` PASS.
- Version and no-GUI bootstrap PASS.
- Real-provider readiness rejects missing real provider setup.
- Base and credentials package dry-runs PASS.
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
- P20 docs link/index PASS.
- Artifact, secret, private-key, certificate, package-output, screenshot, log,
  and signing-material scans PASS.

## Boundaries To Preserve

- Do not commit certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env` files, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
- Do not create, import, purchase, invent, or use production certificates unless
  separately approved.
- Do not run signing commands without explicit safe throwaway/test signing path
  approval and a local-only evidence plan.
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

## Known Limitations For P21

- No approved safe throwaway/test signing path exists.
- No production signing identity, certificate custody execution path, or
  production certificate exists.
- `signtool.exe` is not currently discoverable on PATH.
- No signed artifact verification, timestamp, trust prompt, or revocation
  evidence exists.
- No signed archive candidate is approved for production or transfer.
- No installer, updater, release feed, public support channel, or public release
  path exists.
- No external P20 tester feedback was supplied.
- No real-provider network smoke was run.
- Locked Credential Locker, enterprise-managed keyring policy, unsupported
  backend, remote-session behavior, and broader tester device matrix evidence
  remain limited.

## Recommended P21 Scope

P21 should make an explicit decision:

- approve a safe throwaway/test signing path and run only a narrow local
  rehearsal setup; or
- keep signing blocked and pause signed archive candidate work.

Suggested P21 work if a safe signing path is supplied:

- document approval owner, signing path type, signer identity, certificate
  metadata, private-key custody, timestamp policy, command shape, verification
  commands, cleanup, and evidence retention before running commands;
- run signing only under ignored `tmp\p20-signing-rehearsal\` or successor
  ignored local artifact paths;
- verify hash, Authenticode signature, timestamp policy, and trust label;
- record evidence without certificates, private keys, signed binaries,
  timestamp responses, logs, screenshots, or secrets;
- preserve deterministic base package and explicit credentials package smoke;
- stop immediately on signing, timestamping, verification, trust, cleanup, or
  boundary scan failure.

Suggested P21 work if no safe signing path is supplied:

- keep signing BLOCKED/SKIPPED;
- keep signed archive candidate work blocked;
- preserve private-trial archive handling without producing signed artifacts.

Recommended P21 non-scope:

- public release;
- production certificate purchase, import, custody execution, or use unless
  separately approved;
- committed signing material or signed artifacts;
- installer/updater runtime or release feed;
- SnapLex Cloud, account OAuth, billing, token broker, browser extension, AI
  summary, global hotkeys, broad provider/OCR/capture rewrites, or full
  localization.
