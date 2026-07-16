# AGENTS.md

<!-- codex-init-flow: initialized -->

## Codex Project Workflow

Initialization status: initialized
Initialized at: 2026-06-21 19:24:29 +08:00
Project root: D:\ToolProjects\SnapLex
Initial git remote: git@github.com:onovich/SnapLex.git

Use these workflow skills for routine Codex work in this project:

- `init-flow`: initialize or refresh this project document and workflow configuration.
- `project-git-workflow` / `git-flow`: use for git status, validation, commit, push, stash, ignore, and guarded discard operations.
- `project-ops-workflow` / `ops-flow`: use for environment checks, dependencies, build, test, lint, format, typecheck, dev server, smoke, package, and release dry-run operations.

Prefer the configured wrappers instead of guessing project commands:

```
powershell
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\Status.cmd
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\CommitAndPush.cmd -Message "commit message" -Paths path\to\file,other\file
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\Stash.cmd -StashMessage "reason"
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\DiscardPaths.cmd -ConfirmDangerous -Paths path\to\file
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\StartDevServer.cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Smoke.cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\StopDevServer.cmd
```

Project-specific workflow configs live at:

- `.codex/project-git-workflow.json`
- `.codex/project-ops-workflow.json`

Do not silently fall back to generic git/build/test behavior when those configs exist. Update this section and the workflow configs deliberately when project policy changes.

<!-- /codex-init-flow -->

## SnapLex Planning Entry Points

- Overall delegated implementation guide: `docs/p0_p7_goal_mode_execution_guide.md`.
- Phase plan and round estimates: `docs/phase_plan.md`.
- First phase execution guide: `docs/p0_repository_baseline_goal_guide.md`.
- Latest accepted P7 phase report: `docs/p7_final_validation_report.md`.
- Whole-track closure report: `docs/p0_p7_final_report.md`.
- Post-MVP expansion roadmap: `docs/p7_expansion_roadmap.md`.
- Latest accepted post-MVP guide: `docs/p8_provider_setup_real_translation_goal_guide.md`.
- P7 to P8 handoff: `docs/p7_to_p8_handoff.md`.
- Latest accepted P8 phase report: `docs/p8_final_validation_report.md`.
- P8 to P9 handoff: `docs/p8_to_p9_handoff.md`.
- Latest accepted P9 guide: `docs/p9_apple_inspired_ui_ux_goal_guide.md`.
- Latest accepted P9 report: `docs/p9_final_validation_report.md`.
- P9 to P10 handoff: `docs/p9_to_p10_handoff.md`.
- Latest accepted P10 guide: `docs/p10_secure_credential_account_strategy_goal_guide.md`.
- Latest accepted P10 report: `docs/p10_final_validation_report.md`.
- P10 to P11 handoff: `docs/p10_to_p11_handoff.md`.
- P10 credential/account strategy docs: `docs/p10_credential_strategy_decisions.md`, `docs/p10_secure_storage_notes.md`, `docs/p10_account_strategy.md`.
- Latest accepted P11 guide: `docs/p11_trial_release_hardening_goal_guide.md`.
- Latest accepted P11 report: `docs/p11_final_validation_report.md`.
- P11 to P12 handoff: `docs/p11_to_p12_handoff.md`.
- Latest accepted P12 guide: `docs/p12_private_trial_pilot_feedback_triage_goal_guide.md`.
- Latest accepted P12 report: `docs/p12_final_validation_report.md`.
- P12 to P13 handoff: `docs/p12_to_p13_handoff.md`.
- Latest accepted P13 guide: `docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`.
- Latest accepted P13 report: `docs/p13_final_validation_report.md`.
- P13 to P14 handoff: `docs/p13_to_p14_handoff.md`.
- Latest accepted P14 guide: `docs/p14_manual_environment_source_keyring_validation_goal_guide.md`.
- Latest accepted P14 report: `docs/p14_final_validation_report.md`.
- P14 to P15 handoff: `docs/p14_to_p15_handoff.md`.
- Latest P15 guide: `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`.
- Latest P15 TODO: `docs/p15_todo.md`.
- Latest P15 report: `docs/p15_final_validation_report.md`.
- P15 to P16 handoff: `docs/p15_to_p16_handoff.md`.
