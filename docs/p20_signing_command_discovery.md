# P20 Signing Command Discovery

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: command discovery recorded; signing remains BLOCKED/SKIPPED

P20 records the command discovery result and future command shapes for an
isolated signing rehearsal. Because no explicit safe throwaway/test signing
path is approved, no signing command is run.

## Discovery Results

Command discovery only was run. It did not sign files, generate certificates,
import certificates, call timestamp services, or verify signed output.

Discovery commands and results:

- `Get-Command signtool.exe -ErrorAction SilentlyContinue`: no command found.
- `Get-Command Get-AuthenticodeSignature -ErrorAction SilentlyContinue`: PASS,
  cmdlet available from `Microsoft.PowerShell.Security`.
- `Get-Command Set-AuthenticodeSignature -ErrorAction SilentlyContinue`: PASS,
  cmdlet available from `Microsoft.PowerShell.Security`.
- `Get-Command Get-FileHash -ErrorAction SilentlyContinue`: PASS, function
  available from `Microsoft.PowerShell.Utility`.

The absence of `signtool.exe` is not a P20 failure because signing is currently
BLOCKED/SKIPPED. A future approved rehearsal may either install/discover a safe
Windows SDK `signtool.exe` path or use an explicitly approved PowerShell
test-signing command shape.

## Command Shape Preconditions

Before any future signing command runs:

- `docs/p20_signing_path_approval_record.md` must record APPROVED status with
  all required inputs;
- artifact paths must resolve under `tmp\p20-signing-rehearsal\`;
- unsigned artifact must be built from a clean pushed source commit;
- package variant must be explicit;
- signer identity, custody, timestamp policy, verification commands, cleanup,
  and evidence rules must be recorded;
- no production certificate may be used unless separately approved outside
  P20.

## Future Signing Command Shapes

Preferred Windows SDK shape when `signtool.exe` is explicitly available:

```powershell
signtool sign /fd SHA256 /tr <approved-test-timestamp-url-or-omitted> /td SHA256 /n <approved-test-subject> <artifact-path>
```

PowerShell test-signing shape when an approved test certificate object is
available:

```powershell
Set-AuthenticodeSignature -FilePath <artifact-path> -Certificate <approved-test-certificate> -TimestampServer <approved-test-timestamp-url-or-omitted>
```

For local throwaway rehearsals where timestamping is explicitly out of scope,
the approved record must say timestamp is intentionally skipped and why. A
missing timestamp policy blocks signing.

## Future Verification Command Shapes

For a future signed artifact:

```powershell
Get-AuthenticodeSignature -FilePath <artifact-path>
Get-FileHash -Algorithm SHA256 -Path <artifact-path>
signtool verify /pa /all /v <artifact-path>
```

`signtool verify` is required only when `signtool.exe` is available or a later
gate records an approved equivalent. Verification evidence must be summarized
as sanitized text and must not include screenshots, logs, certificates, private
keys, timestamp responses, or signed binaries.

## Blocked State

Signing command execution remains BLOCKED/SKIPPED because:

- no explicit safe signing-path approval exists;
- no approved test certificate or signing identity exists;
- no private-key custody rule exists;
- no timestamp policy execution exists;
- `signtool.exe` is not currently discoverable on PATH;
- P20 is not allowed to create, import, purchase, invent, or use a production
  certificate.

## Stop Conditions

Do not run signing if:

- approval status is not APPROVED;
- artifact path is outside `tmp\p20-signing-rehearsal\`;
- command would write logs or timestamp responses into tracked paths;
- command requires a certificate, key, PIN, password, or token not recorded in
  the approval record;
- command output would expose private-key paths, secret values, timestamp
  response bodies, or signed binaries in tracked evidence;
- `git status --short` shows unrelated tracked edits.

## Round 4 Self-Checks

Debug self-check:

- The result is explained by the smallest command-discovery workflow:
  `signtool.exe` is not found, Authenticode/hash cmdlets are discoverable, and
  signing remains blocked because approval inputs are missing.
- Success, expected rejection, missing approval, command unavailable, command
  available, no-signing-command, no-artifact, and no-secret states are covered.

Architecture self-check:

- Command discovery does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- Base and credentials package lanes remain separate.
- No production signing, installer, updater, public release, cloud/OAuth,
  browser extension, AI summary, global hotkey, broad provider/OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
