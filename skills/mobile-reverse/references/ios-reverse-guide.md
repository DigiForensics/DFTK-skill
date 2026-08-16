# iOS Reverse Engineering Guide

Authorized analysis of iOS applications (IPA → Mach-O/ObjC/Swift). Use only on apps you are permitted to examine.

## Acquisition & decryption

```text
□ Obtain IPA (App Store via ipatool, or a sanctioned build).
□ Decrypt the fat binary: frida-ios-dump / Clutch (needs a jailbroken device).
□ Record SHA-256 of the IPA and the decrypted binary.
```

## Static analysis

```text
□ class-dump-z / class-dump → ObjC header map (methods, ivars).
□ swift-demangle → recover Swift symbol names.
□ otool -L → linked frameworks; otool -oV → Objective-C runtime info.
□ jtool2 / MachOView → Mach-O load commands, entitlements, code signature.
□ PlistBuddy / defaults → Info.plist (ATS, URL schemes, query schemes, permissions).
□ Ghidra / Hopper → decompile the main binary and embedded .dylibs.
```

## Runtime (authorized device only)

```text
□ Frida / Objection for method tracing and keychain inspection.
□ Hook CCCrypt / SecKeyDecrypt to characterize crypto usage (see mobile-reverse SKILL.md).
□ Inspect entitlements: get-task-allow, keychain-access-groups, app-groups.
```

## Protection-mechanism review

- **Jailbreak detection** — `fork`/`ptrace` (`PT_DENY_ATTACH`), `sysctl` `kern.proc.pid`, file-existence checks (`/bin/bash`, Cydia).
- **Anti-debug** — `ptrace`, `sysctl`, `SIGTRAP`/`isatty` tricks, `Task_for_pid` denial.
- **Obfuscation** — control-flow flattening, string encryption, symbol stripping.
- Deliverable: document the control and its strength; bypass is a lab validation step, not the goal (see `anti-detection-bypass.md`).

## Quality bar

A defensible iOS pass records the binary hash, maps the class structure, reviews protection mechanisms (not just defeats them), and redacts secrets in output. Cross-link `ghidra-reverse/` for decompilation deep-dives and `reverse-exe/` when only a binary is present.
