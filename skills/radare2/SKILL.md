---
name: radare2
description: >-
  Command-line binary analysis with radare2 / r2 — recon, disassembly,
  function/import/string inspection, hex views, light patching, and binary
  diffing for PE/ELF/Mach-O/DEX/WASM. Read-only-first, evidence-preserving. Use
  for CLI reverse engineering, rabin2/rasm2/radiff2/rahash2/rax2 usage, and r2
  scripting. Route to ida-reverse for decompiler / pseudocode work, or to
  reverse-exe / malware-analysis for static malware triage.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - radare2
  - binary-analysis
  - cli
  - forensics
---

# radare2 — CLI binary analysis

Methodology for analyzing `exe` / `dll` / `so` / `elf` / `apk` / `dex` / `wasm`
binaries directly from the command line with `radare2` (`r2`) and its companion
utilities. The goal is to do first-pass recon, function/import/string analysis,
hex inspection, and light modification **without a GUI**, and to feed findings
into DFTK's forensic pipeline.

This is a **methodology skill**. radare2 is an external tool; nothing here is
bundled in the `dftk` wheel. When the artifact under analysis is a generic
file/disk image, prefer `dftk` (read-only tools) for the structured
Observation/Evidence output; use this skill for the binary-specific reasoning.

## Relationship to DFTK

- `dftk hash` is the DFIR-preferred hashing path for any generic artifact; for
  in-binary hashes use `rahash2`.
- For every analysis command here, enable DFTK's audit ledger
  (`--audit <path>` or `DFTK_AUDIT_LOG`) so the *process* is recorded with
  evidence hashes — this is the chain-of-custody record for the binary work.
- When you finish binary triage and the evidence is a protocol stream, hand off
  to `protocol-reverse`; when it is a suspicious sample, hand off to
  `malware-analysis`; when it is a Mach-O/ELF/PE for deeper decompilation, hand
  off to `ida-reverse` / `ghidra-reverse`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** Compute and record a SHA-256 of the original before
   anything else; never mutate the original in place.
2. **Record provenance.** For each conclusion: source command, locator
   (offset/path), value, and hash.
3. **Separate fact from inference.** Use VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
4. **Patch only what you own.** Light patching is permitted only on artifacts
   you are authorized to modify; always work on a copy and log the change in the
   audit ledger.

## Import-table gate (MUST before deep analysis)

For any PE/ELF/Mach-O with an import table, **MUST** complete import inspection
and record it as evidence before entering function-level or dynamic steps:

1. Run `rabin2 -i <sample>` (or the recon output's imports section). For
   DLL/SYS also run `rabin2 -E` and note exports.
2. Write the import table into the audit ledger (suggested id `E-imports` /
   `E-triage-imports`) containing: the repro command, a categorized summary
   (network / file / crypto / process-injection / registry / other suspicious
   API), and — if the table is empty, unparsed, or the tool errored — the raw
   failure output. **Never silently skip.**
3. A "too clean" import table (only base DLLs) means dynamic loading is likely;
   mark it and move to dynamic API tracing.
4. For .NET (no traditional IAT) use an equivalent anchor — dnSpy / IL / metadata
   summary — written into the same evidence slot. Route to `dotnet-reverse`.
5. Packed samples needing IAT rebuild: x86 → ImportREC (or equivalent),
   x64 → Scylla (or equivalent). If rebuild fails, record `E-iat-repair-fail`
   and switch to dynamic API breakpoints; do **not** grind on the static IAT
   forever.

Until the import evidence (or a valid equivalent anchor / IAT-failure bypass) is
recorded, do **not** claim "recon complete" and do **not** enter deeper analysis.

## Environment check (do not assume r2 exists)

```text
r2 -v
rabin2 -v
```

If absent, check common install paths or ask the user to install before guessing
paths. Windows executables: `radare2.exe`, `rabin2.exe`, `rasm2.exe`,
`radiff2.exe`, `rahash2.exe`, `rax2.exe`.

## Workflow 1 — Quick recon

Start with the lightest commands; do not jump straight to full auto-analysis.

```bash
rabin2 -I sample.exe     # format, bits, arch, platform, entry point
rabin2 -z sample.exe     # strings
rabin2 -i sample.exe     # imports  (MUST -> evidence)
rabin2 -E sample.exe     # exports (DLL/SYS)
```

Focus on: file format / bitness / arch / platform, entry point, suspicious
strings (URLs, paths, errors, registry, CLI args), and imports (network / file /
crypto / injection / registry — MUST be logged as evidence).

## Workflow 2 — Interactive function analysis

```text
r2 sample.exe
aaa          # standard auto-analysis (prefer over heavier aaaa)
afl          # list functions
iz           # list strings
iS           # list sections
is           # list symbols
s entry0     # seek to entry point
pdf          # disassemble current function
VV           # visual mode (if terminal supports it)
q            # quit
```

## Workflow 3 — Locate main / key logic

```text
afl~main
afl~sym.
iz~http
iz~error
axt <addr>   # who references this string/address
```

Start from `main`, the entry point, and string references; use `axt` to find
callers, then `s <addr>` + `pdf`.

## Workflow 4 — Hex & memory views

```text
px 64        # 64 bytes hex from current address
pd 20        # disassemble 20 instructions
psz         # read string at current address
pxa         # friendlier hex view
```

## Workflow 5 — Light patch (only on owned artifacts, with a copy)

```text
r2 -w sample.exe   # write mode — only when modification is explicitly required
s 0x401000
wa nop
wa jmp 0x401050
wq
```

Common writes: `wa <asm>` (assemble), `wx <hex>` (raw bytes), `wq` (write &
quit). Back up the original first; if the user did not mention a backup, remind
them once.

## Workflow 6 — Non-interactive automation

```bash
r2 -A -q -c "afl;iz;ii;q" sample.exe
```

- `-A` auto-analyze on start, `-q` quiet, `-c` command string. Prefer a readable
  command order over one unmaintainable mega-string.

## Companion utilities

```bash
rabin2 -I sample.exe     # basic info
rabin2 -S sample.exe     # sections
rabin2 -s sample.exe     # symbols
rabin2 -i sample.exe     # imports
rabin2 -E sample.exe     # exports
rabin2 -z sample.exe     # strings
rabin2 -zz sample.exe    # more detailed strings

rasm2 -d "9090"                       # disassemble
rasm2 -a x86 -b 64 "xor eax, eax"     # assemble

radiff2 old.exe new.exe               # diff two binaries
radiff2 -C old.exe new.exe            # code-only diff

rahash2 -a md5 sample.exe             # hash
rahash2 -a sha256 sample.exe

rax2 0x401000                         # base conversion
rax2 4198400
rax2 -s hello
```

## Recommended analysis order

1. `rabin2 -I` — format / arch / entry.
2. `rabin2 -z` — strings.
3. `rabin2 -i` — imports (**MUST + evidence**).
4. If interactive analysis is needed, enter `r2` only after step 3 is logged.
5. `aaa` → `afl` / `iz` / `pdf`.
6. Locate key functions via string refs, imports, entry flow.

Step 3 is not an optional optimization — it is the gate before deep analysis.

## Notes

- Windows: quote paths with spaces; if `r2` is missing after install, open a new
  terminal (PATH may have just updated). Do not auto-elevate; ask first.
- For web-page JS reverse, use `js-reverse`, not this skill.

## Quality bar

A defensible radare2 pass records the import table as evidence, separates fact
from inference, preserves provenance, and leaves a reproducible command trail
that another analyst can re-run.

---

