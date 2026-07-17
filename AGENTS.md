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
- Latest accepted P15 guide: `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`.
- Latest accepted P15 report: `docs/p15_final_validation_report.md`.
- P15 to P16 handoff: `docs/p15_to_p16_handoff.md`.
- Latest accepted P16 guide: `docs/p16_credential_capable_package_production_hardening_goal_guide.md`.
- Latest accepted P16 report: `docs/p16_final_validation_report.md`.
- P16 to P17 handoff: `docs/p16_to_p17_handoff.md`.
- Latest accepted P17 guide: `docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`.
- P17 pilot/gate evidence: `docs/p17_pilot_lane_plan.md`, `docs/p17_package_candidate_gate_evidence.md`, `docs/p17_tester_feedback_intake.md`, `docs/p17_real_provider_smoke_record.md`, `docs/p17_artifact_transfer_retention_support.md`, `docs/p17_signing_installer_updater_decision.md`, `docs/p17_credential_package_lane_decision.md`, `docs/p17_boundary_scan_evidence.md`.
- Latest P17 report: `docs/p17_final_validation_report.md`.
- P17 to P18 handoff: `docs/p17_to_p18_handoff.md`.
- Latest accepted P18 guide: `docs/p18_signing_distribution_readiness_gate_goal_guide.md`.
- P18 signing/distribution evidence:
  `docs/p18_signing_identity_certificate_custody.md`,
  `docs/p18_signing_verification_policy.md`,
  `docs/p18_signing_rehearsal_record.md`,
  `docs/p18_archive_installer_readiness_decision.md`,
  `docs/p18_rollback_update_policy.md`,
  `docs/p18_artifact_retention_revocation_support.md`,
  `docs/p18_distribution_readiness_decision.md`,
  `docs/p18_boundary_scan_evidence.md`,
  `docs/p18_package_validation_evidence.md`.
- Latest accepted P18 report: `docs/p18_final_validation_report.md`.
- P18 to P19 handoff: `docs/p18_to_p19_handoff.md`.
- Latest accepted P19 guide: `docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`.
- P19 signing rehearsal evidence:
  `docs/p19_signing_path_decision.md`,
  `docs/p19_base_package_control_evidence.md`,
  `docs/p19_credentials_package_candidate_evidence.md`,
  `docs/p19_signing_rehearsal_evidence.md`,
  `docs/p19_signature_verification_policy.md`,
  `docs/p19_signed_archive_stop_conditions.md`,
  `docs/p19_signed_archive_candidate_decision.md`,
  `docs/p19_boundary_scan_evidence.md`.
- Latest accepted P19 report: `docs/p19_final_validation_report.md`.
- P19 to P20 handoff: `docs/p19_to_p20_handoff.md`.
- Latest accepted P20 guide: `docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md`.
- P20 signing path acquisition evidence:
  `docs/p20_signing_path_approval_record.md`,
  `docs/p20_rehearsal_artifact_directory_policy.md`,
  `docs/p20_signing_command_discovery.md`,
  `docs/p20_isolated_rehearsal_evidence.md`,
  `docs/p20_signature_verification_evidence_policy.md`,
  `docs/p20_base_package_control_evidence.md`,
  `docs/p20_credentials_package_control_evidence.md`,
  `docs/p20_boundary_scan_evidence.md`.
- Latest accepted P20 report: `docs/p20_final_validation_report.md`.
- P20 to P21 handoff: `docs/p20_to_p21_handoff.md`.
- Latest accepted P21 guide: `docs/p21_signing_path_unblock_decision_pause_gate_goal_guide.md`.
- P21 signing pause/unblock evidence:
  `docs/p21_signing_path_decision.md`,
  `docs/p21_signing_unblock_requirements.md`,
  `docs/p21_next_phase_recommendation.md`,
  `docs/p21_base_package_control_evidence.md`,
  `docs/p21_credentials_package_control_evidence.md`,
  `docs/p21_boundary_scan_evidence.md`.
- Latest accepted P21 report: `docs/p21_final_validation_report.md`.
- P21 to P22 handoff: `docs/p21_to_p22_handoff.md`.
- Latest accepted P22 guide: `docs/p22_non_signing_private_trial_continuity_tester_support_gate_goal_guide.md`.
- P22 non-signing private-trial continuity evidence:
  `docs/p22_unsigned_private_trial_release_notes.md`,
  `docs/p22_tester_support_intake.md`,
  `docs/p22_feedback_triage_criteria.md`,
  `docs/p22_base_package_continuity_evidence.md`,
  `docs/p22_credentials_package_continuity_evidence.md`,
  `docs/p22_artifact_transfer_retention.md`,
  `docs/p22_boundary_scan_evidence.md`.
- Latest accepted P22 report: `docs/p22_final_validation_report.md`.
- P22 to P23 handoff: `docs/p22_to_p23_handoff.md`.
- Latest accepted P23 guide: `docs/p23_private_trial_feedback_intake_support_loop_gate_goal_guide.md`.
- P23 private-trial feedback/support evidence:
  `docs/p23_feedback_intake_log.md`,
  `docs/p23_privacy_screen_and_triage.md`,
  `docs/p23_support_response_decisions.md`,
  `docs/p23_next_action_register.md`,
  `docs/p23_base_package_continuity_evidence.md`,
  `docs/p23_credentials_package_continuity_evidence.md`,
  `docs/p23_artifact_retention_support_evidence.md`,
  `docs/p23_boundary_scan_evidence.md`.
- Latest P23 report: `docs/p23_final_validation_report.md`.
- P23 to P24 handoff: `docs/p23_to_p24_handoff.md`.
- Latest accepted P24 guide: `docs/p24_non_signing_private_trial_candidate_readiness_feedback_watch_goal_guide.md`.
- P24 non-signing candidate readiness evidence:
  `docs/p24_unsigned_candidate_readiness.md`,
  `docs/p24_feedback_watch_register.md`,
  `docs/p24_support_watch_runbook.md`,
  `docs/p24_base_package_candidate_evidence.md`,
  `docs/p24_credentials_package_candidate_evidence.md`,
  `docs/p24_release_hold_decision.md`,
  `docs/p24_boundary_scan_evidence.md`.
- Latest P24 report: `docs/p24_final_validation_report.md`.
- P24 to P25 handoff: `docs/p24_to_p25_handoff.md`.
- Latest accepted P25 guide: `docs/p25_non_signing_private_trial_feedback_watch_pause_closeout_goal_guide.md`.
- P25 non-signing feedback-watch pause/closeout evidence:
  `docs/p25_rebaseline_signing_pause.md`,
  `docs/p25_feedback_watch_disposition.md`,
  `docs/p25_private_trial_pause_continue_decision.md`,
  `docs/p25_support_readiness_closeout.md`,
  `docs/p25_package_revalidation_evidence.md`,
  `docs/p25_boundary_scan_evidence.md`.
- Latest P25 report: `docs/p25_final_validation_report.md`.
- P25 to P26 handoff: `docs/p25_to_p26_handoff.md`.
- Current planning state: non-signing private-trial feedback watch lane paused;
  no P26 guide is selected unless new feedback, validation drift, a
  planner-approved circulation objective, or safe signing-path inputs arrive.
