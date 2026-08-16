# Obfuscation and sandbox reference

How to approach a packed / obfuscated Windows or Linux executable before deep
reverse engineering. This is triage, not defeat — stay read-only and evidence-preserving.

## Common obfuscations

| Technique | Signal | First response |
|-----------|--------|----------------|
| Control-flow flattening | Huge dispatcher, tiny real blocks | Deobfuscate or note it; don't hand-trace |
| String encryption | Few plaintext strings, decrypt routine | Find decryptor, dump post-decryption |
| Packing / crypter | High entropy section, small entry | Run in sandbox, dump at unpack stage |
| Anti-debug | `IsDebuggerPresent`, `ptrace`, `NtQuery` | Note it; isolate, don't fight it on target |

## Sandbox triage (authorized, isolated)

```text
□ Snapshot a clean VM; run the sample; diff process / file / registry / network
□ Capture API calls (Procmon / strace) for the first N seconds
□ Note persistence, C2 endpoints, dropped files → hand IOCs to malware-analysis
□ NEVER let a sample reach a real network you are not authorized to monitor
```

## Unpacking notes

```text
□ Break at the real entry point (OEP) after the packer resolves imports
□ Dump the decrypted image; re-align sections before analysis
□ Record the packer signature (entropy / section names) for the report
```

## Cross-links
- Crypto identification → `crypto-identification.md`.
- Full sample triage → `../../malware-analysis/examples/worked-triage.md`.
