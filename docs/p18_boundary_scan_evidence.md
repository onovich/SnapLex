# P18 Boundary Scan Evidence

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: PASS

P18 scans confirm that signing/distribution planning did not add tracked
package artifacts, signing material, screenshots, logs, keyring exports, local
app data, tester data, or provider secrets.

## Worktree And Ignored Output Scan

Command:

```powershell
git status --short --ignored
```

Result: PASS.

Observed ignored local paths:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- `snaplex/__pycache__/`
- `snaplex/providers/__pycache__/`
- `snaplex/services/__pycache__/`
- `snaplex/storage/__pycache__/`
- `snaplex/ui/__pycache__/`
- `tests/__pycache__/`
- `tmp/`

These are ignored local outputs or caches. No nonignored package output,
certificate, private key, screenshot, smoke data, log, keyring export, local
app data, tester data, or provider secret was present in the worktree at scan
time.

## Tracked File Inventory

Command:

```powershell
git ls-files
```

Result: PASS.

The tracked inventory contains source, tests, command wrappers, existing PDFs,
and documentation. It includes the P18 policy docs created in this phase. It
does not include package binaries, installer outputs, signing certificates,
private keys, screenshots, logs, keyring exports, smoke app data, local config
or history files, tester data, or provider secrets.

## Signing Material File Scan

Command:

```powershell
rg --files -g *.pfx -g *.p12 -g *.pem -g *.pvk -g *.spc -g *.cer -g *.crt -g *.key
```

Result: PASS. No matching signing-material files were found.

## Binary Artifact File Scan

Command:

```powershell
rg --files -g *.exe -g *.msi -g *.zip -g *.7z -g *.log -g *.png -g *.jpg -g *.jpeg
```

Result: PASS. No matching package, log, or screenshot artifacts were found in
nonignored files.

## Private-Key And Token Marker Scan

Command:

```powershell
rg -n --hidden --glob !.git/** --glob !docs/** --glob !README.md --glob !AGENTS.md --glob !packaging/README.md "BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY|PRIVATE KEY-----|CERTIFICATE-----|sk-[A-Za-z0-9]{20,}" .
```

Result: PASS. No private-key blocks, certificate blocks, or raw OpenAI-style
secret token markers were found outside documentation allowlists.

## Policy Keyword Scan

Command:

```powershell
rg -n "(\.pfx|\.p12|\.pem|\.pvk|\.spc|\.cer|\.crt|\.key|\.exe|\.msi|\.zip|\.7z|\.log|keyring export|signed artifact|private key)" docs README.md AGENTS.md scripts packaging snaplex tests
```

Result: PASS with expected documentation references.

Matches were policy, guide, README, packaging README, historical evidence, test,
or source references describing commands and forbidden artifact classes. No
match represented committed signing material, package output, secret-bearing
log, screenshot, keyring export, tester data, or provider secret.

## Round 9 Self-Checks

Debug self-check:

- The evidence is explained by the smallest boundary workflow: worktree scan,
  tracked inventory, signing-material file scan, binary/log/screenshot scan,
  private-key marker scan, and policy keyword review.
- Success, ignored local output, no-match scan, expected documentation match,
  skipped signing, and no-secret states are covered.

Architecture self-check:

- Boundary scanning does not change runtime, provider, credential, settings,
  history, capture, OCR, UI, packaging, or trial readiness behavior.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
