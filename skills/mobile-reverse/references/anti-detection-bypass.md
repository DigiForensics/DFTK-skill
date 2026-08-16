# Anti-Detection & Protection-Mechanism Review

Mobile apps deploy runtime guards (SSL pinning, root/jailbreak detection, anti-debug, obfuscation) to raise the bar on tampering. In an authorized assessment the *deliverable is the review of these controls* — what they check, how strong they are, and whether they meaningfully protect the asset. Disabling a control is a lab step used to **validate** that the guard actually fires; it is not the end goal.

## What to document per control

| Field | Example |
|---|---|
| Control | SSL certificate pinning |
| Mechanism | `TrustManager` override / `NSURLSession` delegate pin check |
| Trigger | Network call to `api.target.com` |
| Bypass (lab) | Objection `android sslpinning disable` / Frida pin hook |
| Assessment | Pin present but skippable on rooted device → medium |
| Evidence | SHA-256, command, captured output (secrets redacted) |

## Controls to review

- **SSL pinning** — static pin vs dynamic, cert vs public-key, fallback behaviour on pin mismatch.
- **Root / jailbreak detection** — file checks, `ptrace`/`sysctl`, package-manager presence, emulator fingerprints.
- **Anti-debug** — `ptrace(PT_DENY_ATTACH)`, `sysctl` `kern.proc.pid`, `SIGTRAP`/`isatty`, runtime integrity.
- **Obfuscation** — symbol stripping, string encryption, control-flow flattening; note residual strings/debuggable flag.
- **Tamper / repack** — signature verification, `debuggable=true` check, hook-detection.

## Lab validation, not weaponization

```bash
# Authorized-device only; record everything.
objection -g "com.target.app" explore
  android sslpinning disable
  ios jailbreak disable
# Confirm the app still functions without the guard → guard was the only control.
```

## Quality bar

A defensible review enumerates each control, explains its mechanism, validates (in a lab) whether it actually fires, rates its strength, and captures redacted evidence. It does not ship bypass tooling as a result; it reports the residual risk. Enable the DFTK 3.3.0 audit ledger for any local instrumentation so the session is reproducible.
