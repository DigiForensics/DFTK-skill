---
name: dotnet-reverse
description: >-
  .NET / C# binary reverse engineering — managed-assembly identification,
  deobfuscation (de4dot), dnSpyEx / ILSpy static analysis, and IL-level
  inspection. Read-only-first, evidence-preserving. Use for managed PE / .exe /
  .dll, ConfuserEx / SmartAssembly / Babel / Eazfuscator / .NET Reactor, and for
  authorized analysis of .NET malware loaders or red-team tooling. Not for native
  binaries (use reverse-exe / ida-reverse).
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - dotnet
  - csharp
  - deobfuscation
  - forensics
  - malware
---

# .NET / C# reverse engineering

Methodology for analyzing .NET / C# compiled products (managed PE, `.exe` /
`.dll`), including deobfuscation and IL-level inspection. .NET malware loaders,
info-stealers, and Red-team tooling (authorized IR context only) are common
subjects; so are benign apps whose logic you own or are authorized to assess.

This is a **methodology skill**. The tools are external; nothing here is bundled
in the `dftk` wheel.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the assembly; `de4dot` handles
  in-assembly deobfuscation.
- A .NET sample that is actually a native payload (IL2CPP / NativeAOT) → route to
  `reverse-exe` / `ida-reverse`. A `.so` inside an APK → route to `apk-reverse`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the original; keep the original immutable for
   comparison.
2. **Deobfuscate first when packed.** Run `de4dot` before static analysis so
   strings/control-flow are readable; keep both the original and the `-clean`
   output.
3. **IL over C# for judgments.** The C# view can distort compiler-generated
   state machines / async / yield; verify key decisions in the IL view.
4. **Record provenance.** Each finding cites: method, IL offset, the observed
   logic, and the repro path.
5. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
6. **Patch only owned artifacts.** IL patching is permitted only for assemblies you
   are authorized to modify; log the change in the audit ledger.

## Tool chain

| Capability | Preferred | Notes |
|------------|-----------|-------|
| Decompile + debug + patch | **dnSpyEx** | The reference GUI; only one with an IL editor. Use the Ex fork (old dnSpy is unmaintained). |
| Lightweight CLI / headless | **ILSpy** (`ilspycmd`) | Batch / scripted / Linux-macOS. |
| Deobfuscation | **de4dot** | Default for ConfuserEx / SmartAssembly / Babel / Eazfuscator / .NET Reactor. |
| Packer identification | **Detect It Easy (DIE)** / `file` | Identify the protector before choosing `de4dot` flags. |
| Programmatic IL | **dnlib** | C# scripts to edit metadata / string decryptors in bulk. |

## Six-phase workflow

### 1. Identify (confirm managed)

Do not treat a native PE as .NET. Confirm the CLR header:

```bash
# generic
strings target.exe | grep -iE "mscoree|_CorExeMain|mscorlib|System\\."
# Windows
powershell -c "[System.Reflection.AssemblyName]::GetAssemblyName('target.exe')"
```

.NET markers: `Data Directory[14]` (CLR Runtime Header) non-zero; `mscoree.dll`
import / `_CorExeMain` entry; `#~`, `#Strings`, `#US`, `#GUID`, `#Blob`
metadata streams; `mscorlib` / `System.Private.CoreLib` strings.

**NativeAOT exception:** compiles to native with no CLR header, but retains
`System.Private.CoreLib` strings and reconstructed type metadata → route to
`reverse-exe` / `ida-reverse` (this module only flags it).

### 2. Detect (protector)

```bash
diec target.exe     # Detect It Easy CLI
```

See `references/obfuscators.md` for per-protector `de4dot` behavior.

### 3. Deobfuscate

```bash
de4dot target.exe -o target-clean.exe
de4dot --type cfze target.exe     # ConfuserEx (when auto-detect fails)
de4dot --type sa target.exe       # SmartAssembly
de4dot --detect target.exe        # see what it detects
```

Output `target-clean.exe`; analyze that. **Keep the original** for comparison.

### 4. Static analysis

Load the cleaned sample in dnSpyEx:

- **C# view** — quick class/structure/method browsing and string location.
- **IL view** — required for key decisions, crypto logic, and state machines (right
  click → Edit IL or open the IL view).
- Entry: `Main` / `Startup` / module initializer (`Module .cctor`).
- Key logic: search `flag`, `password`, `verify`, `check`, `encrypt`, `http`,
  `Config`.

```text
locate string -> back-reference -> method that uses it -> IL view for the decision
```

### 5. Dynamic (optional, authorized)

dnSpyEx debugger: attach / launch, set breakpoints on key methods, observe at
runtime:

- decrypted plaintext strings (many protectors decrypt at runtime);
- C2 addresses / config decryption results;
- exception-driven control flow (anti-debug often hides the real path in
  try/catch).

.NET dynamic debugging is far friendlier than native — you see object values and
string contents directly.

### 6. Patch (owned artifacts only)

```text
dnSpyEx -> right-click method -> Edit Method (C#) or Edit IL
  - flip decision: ldc.i4.0 -> ldc.i4.1
  - change constant: edit string/number directly
  - remove check: nop out the block
File -> Save Module -> replace (work on a copy)
```

**IL patch reliability > C# patch:** C# recompile can fail (missing references,
syntax); IL editing almost never distorts. See `references/common-workflow.md`.

## When to route out

- IL2CPP Unity → `reverse-exe` (native, not dnSpy).
- NativeAOT → `reverse-exe` / `ida-reverse`.
- Pure native PE (no CLR) → `reverse-exe` / `ida-reverse`.
- Need to migrate symbols to another version → `binary-diff`.

## Quality bar

A complete .NET pass confirms managed identity (or routes out), deobfuscates
packed samples before deep analysis, verifies key logic in the IL view (not just
C#), and keeps the original + cleaned + patched artifacts reproducible.

---

