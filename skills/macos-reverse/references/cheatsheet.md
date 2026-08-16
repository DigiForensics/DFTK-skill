# macOS / Mach-O triage cheatsheet

Command reference for `macos-reverse`. Analyze a copy; `dftk hash` the original first.
iOS/IPA routes to `mobile-reverse`. Do not bypass TCC / Hardened Runtime on systems
you are not authorized to test.

## Signature & notarization

```bash
file target                                   # Mach-O / universal / .app bundle
codesign -dv --verbose=4 target               # identity, Team ID, flags
spctl -a -vv target 2>&1                      # Gatekeeper assessment
otool -L target                               # linked dylibs + rpath
dftk hash target
```

Record: signing identity, notarization status, Hardened Runtime flags
(`runtime`, `library-validation`), and rpath / `LC_LOAD_DYLIB` set.

## Static

```text
□ class-dump / dsdump        — Objective-C @interface / @protocol surface
□ swift-demangle             — recover Swift symbol names
□ strings + XPC service names + TCC-sensitive API (AddressBook, Photos, FullDiskAccess)
□ Hopper / Ghidra / IDA      — decompilation
□ jtool2                    — Mach-O internals, entitlements, LC inspection
```

## Dynamic (authorized, isolated)

```bash
# Behavior observation without a debugger
sudo fs_usage -w -f filesys  # file access
log stream --predicate 'process == "target"' --level debug
# In-depth
lldb target                  # or Frida
```

## Hardened Runtime / TCC checklist

| Control | What to check | Evidence to record |
|---------|---------------|--------------------|
| Hardened Runtime | `codesign -dv` flags | `runtime` / `library-validation` present? |
| Entitlements | `codesign -d --entitlements :-` | `com.apple.security.*`, `get-task-allow` |
| TCC usage | string xref for protected APIs | Which privacy domain is touched |
| LaunchItem | `~/Library/LaunchAgents`, `…/LaunchDaemons` | Persistence plist + label |
| Notarization | `spctl -a -vv` | ticket status / Team ID |

## Cross-links
- DFTK MCP: `../../../references/mcp-setup.md`.
- iOS/IPA runtime review: `../../mobile-reverse/references/`.
- Deep decompilation: `../../ghidra-reverse/`, `../../ida-reverse/`.
- Suspicious sample: `../../malware-analysis/`.
