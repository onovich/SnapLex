# P21 Signing Unblock Requirements

Date: 2026-07-17
Phase: P21 Signing Path Unblock Decision Or Pause Gate
Status: PAUSED - unblock inputs missing

P21 records signing as PAUSED. This document lists the exact inputs required
before a later phase may prepare or run any signing rehearsal. P21 itself does
not run signing commands, create/import/purchase/invent/use certificates, call
timestamp services, or produce signed artifacts.

## Current Decision

Signing remains paused because no explicit safe throwaway/test signing path
approval was supplied after P20.

Current trust label: `unsigned-private-trial`.

The `base` package remains deterministic and keyring-free. The `credentials`
package remains explicit and private-trial only.

## Required Unblock Inputs

A later phase may change signing from PAUSED to approved for rehearsal only
after all of these inputs are supplied and recorded before commands run:

1. Explicit approval record
   - approval owner;
   - approval date;
   - approving thread, issue, or document;
   - scope limited to safe throwaway/test signing unless production signing is
     separately approved.

2. Signing path type
   - local throwaway certificate, hardware token test certificate, managed
     signing sandbox, or another named non-production path;
   - confirmation that the path is safe for private rehearsal;
   - confirmation that it is not public release authorization.

3. Signer identity and certificate metadata
   - signer identity label;
   - certificate subject, issuer, and non-secret thumbprint or test identifier
     when a certificate already exists;
   - explicit proof that no production certificate is used unless separately
     approved outside the rehearsal phase.

4. Certificate source and custody
   - source of test certificate or managed signing identity;
   - private-key custody rule;
   - cleanup and revocation/disposal rule;
   - confirmation that certificates and private keys are never committed,
     exported into git, logged, screenshot, or packaged.

5. Ignored local artifact path
   - local-only directory for unsigned and signed rehearsal files;
   - proof the directory is ignored by git;
   - cleanup rule after rehearsal evidence is recorded.

6. Command plan
   - exact signing tool path or command family;
   - exact command shape with placeholders only;
   - no raw secrets, private keys, passwords, tokens, or provider credentials in
     command text;
   - stop condition if the command would write outside ignored local paths.

7. Timestamp policy
   - timestamp skipped for local throwaway rehearsal, or;
   - approved test-safe timestamp endpoint and network approval;
   - expected evidence without timestamp response files in git.

8. Verification policy
   - hash verification command;
   - Authenticode or equivalent signature verification command;
   - expected unsigned/signed/trust label;
   - failure criteria for missing, invalid, expired, or unexpected signatures.

9. Evidence retention policy
   - commit only non-secret Markdown evidence;
   - record command names, pass/fail status, hashes when safe, and decision
     summary;
   - do not commit certificates, private keys, signed binaries, package
     outputs, timestamp responses, screenshots, logs, `.env`, keyring exports,
     tester data, local app data, smoke data, OCR caches, or provider secrets.

10. Cleanup and boundary scans
    - post-rehearsal cleanup command plan;
    - artifact scan;
    - secret scan;
    - private-key and certificate scan;
    - package-output, screenshot, log, and signing-material scan.

## Inputs That Do Not Unblock Signing

These are insufficient by themselves:

- a general desire to sign SnapLex;
- `signtool.exe` becoming available;
- a local self-signed certificate invented by the executor;
- a production certificate without separate production-signing approval;
- a timestamp endpoint without explicit network approval and retention policy;
- a package build that succeeds without signing;
- a private-trial transfer need without approved signing custody.

## Stop Conditions For A Later Phase

A later signing phase must stop before running signing commands if:

- any required unblock input is missing;
- artifact paths are not ignored;
- command text would reveal a secret;
- a command would write signed artifacts into git-tracked paths;
- a certificate or private key would be exported or committed;
- timestamping would require unapproved network use;
- verification or cleanup commands are not defined;
- boundary scans cannot be run afterward.

## P21 Self-Checks

Debug self-check:

- The PAUSED state is explained by the smallest evidence set: P20 had no safe
  signing path, P21 received no new approval inputs, and the guide forbids
  signing commands in P21.
- Success, expected rejection, missing approval, paused signing, no
  certificate, no signing command, no timestamp, no-artifact, and no-secret
  states are covered.

Architecture self-check:

- This document changes only release decision evidence.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
