---
name: apk-reverse
description: >-
  Tool-driven Android APK reverse engineering: jadx Java decompilation, apktool
  unpacking / smali & Manifest inspection, Frida dynamic hooking, and native .so
  triage. Read-only-first; modification only for apps you own or are authorized to
  assess. Pairs with the read-only `apk` module (static forensic entry-point /
  native-secret triage) and with `ida-reverse` / `radare2` for the .so layer.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - android
  - apk
  - frida
  - forensics
---

# APK reverse engineering (tool methodology)

Practical workflow for analyzing an Android application package with
`jadx`, `apktool`, `frida`, and `adb`. It complements the read-only `apk`
module: that module covers static forensic entry-point / native-secret triage
without running the app; this module covers the deeper tool-driven workflow
including optional dynamic observation.

This is a **methodology skill**. The tools are external; nothing here is bundled
in the `dftk` wheel. When the task is *static-only* forensic triage (no
execution), prefer the `apk` module.

## Relationship to DFTK

- For every command here, enable DFTK's audit ledger (`--audit <path>` or
  `DFTK_AUDIT_LOG`) so the process is recorded with evidence hashes.
- `dftk hash` is the DFIR-preferred hashing for the APK file itself; `apktool` /
  `jadx` handle in-package artifacts.
- When core logic lives in a `.so`, hand off to `ida-reverse` (deep decompile) or
  `radare2` (quick triage). When the task is pure static forensic triage, hand
  off to `apk`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the APK; analyze a copy, never the original.
2. **Dynamic only on an authorized device / isolated emulator.** Do not run the
   app on the analysis host. Confirm the device/scope is authorized.
3. **Record provenance.** Each finding cites: tool, command, locator (class /
   method / smali offset / `.so` symbol), value, hash.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
5. **Modify only what you own.** Patching / repackaging an APK is permitted only
   for apps you are authorized to modify; always work on a copy and log the
   change in the audit ledger. Never ship a bypass for third-party controls you
   are not authorized to alter.

## Pre-flight tool check

```bash
jadx --version
apktool --version
frida-ps -U          # requires a connected device / emulator
adb devices
java -version
```

## Workflow 1 — Triage (no modification)

1. Decompile Java: `jadx -d jadx_out app.apk`
2. Unpack resources/smali: `apktool d app.apk -o apktool_out`
3. Inspect `AndroidManifest.xml`, the main `package`, `application` /
   `activity` / `service` / `receiver`, and whether `lib/` contains `.so`.
4. Note the launcher activity, requested permissions, exported components, and
   any `System.loadLibrary("…")` calls (native entry).

## Workflow 2 — Java logic observation

Read from `jadx_out` first:

- `MainActivity`, `Application`, login / network / crypto / risk-control classes,
  third-party SDK init.

Key terms to grep: `login`, `sign`, `encrypt`, `cipher`, `token`, `root`,
`certificate`, `trust`, `okhttp`, `retrofit`, `webview`.

If the Java is readable, locate business logic here before going deeper.

## Workflow 3 — Smali & resource confirmation

When `jadx` output is incomplete, heavily obfuscated, or you need to actually
patch:

- Inspect `smali*/`, `res/values/strings.xml`, `AndroidManifest.xml`.
- Common patch targets (authorized apps only): `android:exported`, debug flags,
  risk-control return values, login-verification branches, cert-pinning branches.

## Workflow 4 — Rebuild & install (authorized apps only)

```bash
apktool b apktool_out -o rebuilt.apk
```

Then align + sign (`zipalign`, `apksigner`) and optionally `adb install -r`.
Signing requires a keystore you control; never reuse or abuse a vendor key.

## Workflow 5 — Dynamic observation (Frida)

Use dynamic observation to confirm static hypotheses (not to "defeat" controls
on apps you do not own):

```bash
frida-ps -U
frida -U -f com.example.app -l hook.js
frida-trace -U -f com.example.app -j '*!*certificate*'
```

Principles: hook the Java layer first; print arguments/return values before
deciding whether to alter them. Record every hook target and observed value. See
`references/frida-recipes.md` for starter scripts.

## Workflow 6 — Native `.so` diversion

If the APK carries a critical `.so`:

- Locate it via `apktool` / `jadx` (`lib/**/*.so`).
- Quick triage / string & export inspection → `radare2`.
- Deep decompile, renaming, type recovery → `ida-reverse`.

Divert to native as soon as: Java is only a JNI wrapper, core signing/risk logic
is absent from Java, `System.loadLibrary()` hides the logic, or cert-pinning /
risk-control lives in the `.so`.

## Output requirements

State at minimum:

- entry components and key classes;
- where the sensitive logic lives (Java / smali / `.so`);
- confirmed sensitive points (login, signing, root, SSL, WebView, JNI);
- if patched: what changed (authorized app only);
- if hooked: which class/method/export was observed.

## Quality bar

A complete APK pass preserves provenance, separates fact from inference,
keeps the original immutable, and — for any dynamic step — confirms authorized
scope before executing.

---

