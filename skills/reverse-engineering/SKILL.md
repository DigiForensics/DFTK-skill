---
name: reverse-engineering
description: General reverse engineering methodology for compiled, obfuscated, packed, or virtualized targets — binaries, APKs, WASM, firmware, custom VMs, bytecode, and anti-analysis logic. Use when the real blocker is understanding how a target works (not exploiting it). Read-only analysis; pivot to specialized sub-skills for deeper work.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - reverse-engineering
  - static-analysis
  - dynamic-analysis
  - anti-analysis
  - obfuscation
---

# Reverse Engineering — General Methodology

A methodology skill for understanding how a compiled/obfuscated/packed/virtualized target works. The goal is comprehension and characterization (and, where authorized, detection). It is **not** an exploitation skill: once the algorithm, protocol, or logic is understood, hand off to the appropriate specialist (malware-analysis, protocol-reverse, reverse-exe, mobile-reverse) rather than building weaponization.

## Operating contract

- Default to a **local, isolated, authorized** context (CTF/crackme/training/own binary). Do not expand scope without evidence.
- Prefer offline analysis; do not execute untrusted samples, mutate originals, or perform state-changing actions unless explicitly authorized on a copy.
- Work on copies; record SHA-256 and reproducible commands. Enable the DFTK 3.3.0 audit ledger for process provenance.
- Drive the task with the user's actual claim; present numbered next-step menus at the end of each phase.

## Problem-solving workflow

1. **Strings first** — `strings -a`, `rabin2 -z/-zz`; many easy targets leak plaintext.
2. **Dynamic quick wins** — `ltrace`/`strace` often reveals secrets without reversing.
3. **Frida hooking** — hook `strcmp`/`memcmp` to capture expected values.
4. **Symbolic execution** — `angr` solves many flag-checkers automatically.
5. **Emulation** — `Qiling` for foreign-arch or heavy anti-debug without artifacts.
6. **Map control flow** before modifying execution.
7. **Automate** via `r2pipe`/Frida/angr/Python.
8. **Validate** by comparing decompilers (dogbolt.org side-by-side).

## Quick wins
```bash
strings binary | grep -E "flag\{|CTF\{|secret|password"
rabin2 -z binary | grep -i flag
ltrace ./binary; strace -f -s 500 ./binary
xxd binary | grep -i flag
```

## Initial analysis
```bash
file binary            # type + arch
checksec --file=binary # mitigations (useful context)
chmod +x binary
```

## Memory dumping strategy
Let the program compute the answer, then capture it: break at the final comparison, supply any input of correct length, and dump the computed value.

## Comparison direction (critical)
- `transform(flag) == stored` → reverse the transform.
- `transform(stored) == flag` → the flag is the transformed data; just apply the transform to the stored target.

## Common encryption patterns
XOR single-byte → XOR known plaintext (`flag{`) → RC4 with hardcoded key → custom permutation+XOR → position-indexed XOR layered with a repeating key.

## Tool quick reference
```bash
r2 -d ./binary      # radare2 debug
aaa; afl; pdf @ main # analyze / list / disassemble
# Ghidra headless: analyzeHeadless project/ tmp -import binary -postScript script.py
# IDA: ida64 binary
```

## Pivot guidance
- Need deep IDA decompilation → `reverse-exe` / `ida-reverse`.
- Need radare2 CLI recon → `reverse-exe` / `radare2`.
- APK layer → `mobile-reverse` (DFTK also parses APK).
- Need Frida/angr dynamic execution → dynamic references below.
- Bypass anti-debug → anti-analysis references.
- Language specifics (Go/Rust/Python/WASM/.NET) → language references.
- CTF patterns → patterns references.

## Domain references — load only when needed
- `references/index.md` — map of all 25 topic areas and when to use each.
- `references/anti-analysis.md` — debugger/VM/sandbox/DBI detection and bypass strategies.
- `references/languages-compiled.md` — Go (GoReSym, goroutines, embed.FS), Rust (demangling, panic strings), Swift, Kotlin/JVM, C++ vtable/RTTI.
- (Reference-only, noted for depth): tools, tools-dynamic, tools-advanced, patterns(-ctf*), languages, languages-platforms, platforms, platforms-hardware, field-notes.

## Quality bar
A good RE pass starts from strings/dynamic quick wins, maps control flow before acting, validates across decompilers, and answers the claim with a reproducible chain. It never fabricates an import table or asserts "benign" from absence of observed behavior.

---

