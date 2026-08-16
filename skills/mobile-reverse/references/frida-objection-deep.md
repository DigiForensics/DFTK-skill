# Frida + Objection — Deep Usage

Runtime instrumentation for authorized mobile analysis. Framing here is *review and characterization*: identify what an app does at runtime, capture evidence, and assess protection mechanisms. Use only on apps and devices you are authorized to test.

## Setup

- Install Frida server on the device (rooted Android / jailbroken iOS) or inject the Frida Gadget (no-root: repackage `.so`/`.dylib`, re-sign, install).
- Verify: `frida-ps -U` lists processes.

## Objection (fast, scripted)

```text
objection -g "com.target.app" explore
  android sslpinning disable          # validate pinning control in a lab
  ios sslpinning disable
  android root disable                # observe app behaviour without root checks
  ios jailbreak disable
  android hooking list classes
  android hooking watch class_method "com.x.Y.method" --dump-args --dump-return
  android keystore list / ios keychain dump
  env                                      # list env, ls, sqlite connect
```

## Frida (custom scripts)

```javascript
// Trace a method and its arguments
Java.perform(function () {
  var C = Java.use("com.target.Crypto");
  C.encrypt.implementation = function (a, b) {
    console.log("[encrypt] a=" + a + " b=" + hexdump(b));
    return this.encrypt(a, b);
  };
});
```

```bash
# CLI one-liners
frida -U -f com.target.app -l hook.js          # spawn + inject
frida-trace -U -i "open*" com.target.app        # trace by name
```

## Evidence hygiene

- Record the app SHA-256 and the exact command/script before running.
- Capture console output to a file; redact keys/tokens/PII before sharing.
- Enable the DFTK 3.3.0 audit ledger for any local tooling so the session is reproducible.

## Quality bar

A defensible dynamic pass states what was instrumented and why, captures the relevant method I/O as evidence, and assesses the protection mechanism rather than merely disabling it. Bypass scripts are a *lab validation* of a control, not the deliverable.
