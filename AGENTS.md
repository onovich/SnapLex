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
- Latest accepted phase report: `docs/p7_final_validation_report.md`.
- Whole-track closure report: `docs/p0_p7_final_report.md`.
- Post-MVP expansion roadmap: `docs/p7_expansion_roadmap.md`.
