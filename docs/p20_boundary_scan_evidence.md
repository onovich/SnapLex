# P20 Boundary Scan Evidence

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: PASS

P20 scans the repository boundary after signing was recorded as
BLOCKED/SKIPPED and after base/credentials package lane validation. Generated
package outputs and smoke data remain ignored local artifacts only.

## Git Boundary

Command:

```powershell
git status --short --ignored
```

Result: PASS.

Only ignored local outputs and caches were present:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- package `__pycache__/` directories
- `tests/__pycache__/`
- `tmp/`

No nonignored package output, signing material, screenshot, log, local app data,
smoke data, OCR cache, keyring export, tester data, `.env`, provider secret, or
signed artifact appeared.

## Signing Material Scan

Command:

```powershell
rg --files -g "*.pfx" -g "*.p12" -g "*.pem" -g "*.pvk" -g "*.spc" -g "*.cer" -g "*.crt" -g "*.key"
```

Result: PASS with no matches.

No certificate, private-key, or signing-material file path was found.

## Package, Screenshot, And Log Artifact Scan

Command:

```powershell
rg --files -g "*.exe" -g "*.msi" -g "*.zip" -g "*.7z" -g "*.log" -g "*.png" -g "*.jpg" -g "*.jpeg"
```

Result: PASS with no matches.

No unignored package output, archive, screenshot, or log file path was found.

## Private-Key, Certificate, And Secret Marker Scan

Command:

```powershell
rg -n --hidden --glob "!.git/**" --glob "!docs/**" --glob "!README.md" --glob "!AGENTS.md" --glob "!packaging/README.md" "BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY|PRIVATE KEY-----|CERTIFICATE-----|sk-[A-Za-z0-9]{20,}" .
```

Result: PASS with no matches.

No private-key block, certificate block, or OpenAI-style secret token marker was
found outside documentation allowlists.

## Policy Keyword Scan

Command:

```powershell
rg -n --hidden --glob "!.git/**" --glob "!build/**" --glob "!dist/**" --glob "!snaplex-smoke-data/**" --glob "!tmp/**" --glob "!.mypy_cache/**" --glob "!.pytest_cache/**" --glob "!.ruff_cache/**" --glob "!**/__pycache__/**" "pfx|p12|pem|private key|certificate|signed binary|timestamp response|provider secret|sk-" .
```

Result: PASS with expected policy/documentation references only.

The scan matched tracked documentation such as `README.md`, `AGENTS.md`,
`TRY.md`, phase guides, handoffs, and P20 policy/evidence files. Matches were
instructions, forbidden-item lists, prior phase evidence, or commit/document
references. They were not raw secrets, certificate blocks, private keys,
timestamp response bodies, signed binaries, package outputs, screenshots, or
logs.

## Decision

Decision: PASS.

P20 boundary rules are preserved:

- no signing command ran;
- no certificate, private key, signed binary, timestamp response, screenshot,
  log, `.env`, keyring export, tester personal data, local app data, smoke
  data, OCR cache, package output, or provider secret is committed;
- generated package and smoke outputs remain ignored local artifacts;
- `base` remains deterministic and keyring-free;
- `credentials` remains explicit and private-trial;
- signing remains BLOCKED/SKIPPED until explicit safe-path approval exists.

## Round 9 Self-Checks

Debug self-check:

- The evidence is explained by the smallest boundary workflow: check git
  ignored state, scan signing-material file extensions, scan package/log/
  screenshot extensions, scan private-key/certificate/secret markers, and
  classify broad keyword matches as policy text only.
- Success, expected rejection, missing approval, ignored generated outputs,
  no-signing-material, no-package-artifact, no-secret, and no-artifact states
  are covered.

Architecture self-check:

- Boundary scans do not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- Base and credentials package lanes remain separate.
- No production signing, installer, updater, public release, cloud/OAuth,
  browser extension, AI summary, global hotkey, broad provider/OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, signing log, package artifact, or screenshot is
  introduced.
