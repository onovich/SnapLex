# P10 TODO

P10 goal: define and implement the first secure credential strategy for
SnapLex real-provider setup while preserving env-var users, provider boundaries,
deterministic tests, and no-secret repository hygiene.

Status: in execution.

Executable guide: `docs/p10_secure_credential_account_strategy_goal_guide.md`

Estimated budget: 16 conversation rounds.

## Tasks

- [x] Revalidate the accepted P9 baseline.
- [x] Produce credential threat model and strategy decisions.
- [x] Add credential reference/status models and credential service/store
  boundaries.
- [x] Preserve existing environment-variable provider credentials.
- [x] Add optional lazy OS keyring storage path or document a concrete blocker.
- [x] Ensure config stores credential references only, not raw values.
- [ ] Route provider readiness and Test Connection through credential
  boundaries.
- [ ] Update Settings presenter/UI for credential source, readiness, save, and
  delete without echoing secrets.
- [ ] Update real/fake trial readiness guardrails for the accepted credential
  boundary.
- [ ] Document env var, OS keyring, SnapLex Cloud/token broker, and provider
  account/OAuth tradeoffs.
- [ ] Preserve P9 GUI smoke, P8 provider smoke, no-GUI bootstrap, and package
  dry-run.
- [ ] Produce P10 final validation report.
- [ ] Produce P10 to P11 handoff.

## Deferred Outside P10

- Production SnapLex Cloud, account OAuth, billing, token broker, or remote
  accounts.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to credential resolution.
- OCR/capture rewrites.
- Full localization implementation.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, or secrets.
