---
name: ida-reverse
description: >-
  IDA Pro decompilation workflow for authorized binary analysis — survey, import
  inspection, pseudocode recovery, cross-references, data-flow tracing, and
  structured annotation. Read-only-first, evidence-preserving. Use when a sample
  needs deep decompilation that radare2 cannot provide, or when migrating symbols
  to a new version (see binary-diff). Commercial IDA Pro required.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - ida-pro
  - decompilation
  - forensics
---

# IDA Pro decompilation workflow

Methodology for using **IDA Pro** (optionally via the `idalib-mcp` HTTP bridge)
to decompile and reason about a binary you are authorized to analyze. IDA's
pseudocode, cross-references, and type recovery make it the right tool when
`radare2` triage is not enough — deep algorithm recovery, large call graphs, and
symbol migration.

This is a **methodology skill**. IDA Pro is a commercial product; nothing here is
bundled in the `dftk` wheel. When the artifact is a generic file, prefer `dftk`
for structured Observation/Evidence output.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working
  so the analysis process is recorded with evidence hashes.
- `dftk hash` is the DFIR-preferred hashing for the binary file; IDA handles
  in-binary reasoning.
- Hand off to `binary-diff` when you have a previous version's symbols to migrate;
  to `radare2` for quick CLI triage; to `malware-analysis` for suspicious samples.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the original before opening in IDA.
2. **Survey before deep dive.** Always run a survey (Step 3) and log imports as
   evidence before drawing conclusions.
3. **Record provenance.** Each finding cites: function/address, the decompiled
   logic, and the repro path.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
5. **Modify only owned artifacts.** Patching in IDA is permitted only for binaries
   you are authorized to modify; log every patch in the audit ledger.

## Import-table gate (MUST before deep analysis)

As with `radare2`, **MUST** inspect and record the import table before entering
deep conclusions:

1. Run a survey / import query (in `idalib-mcp`: `idapro_survey_binary` or
   `idapro_entity_query(kind="imports")`).
2. Write the categorized import summary into the audit ledger (`E-imports` /
   `E-triage-imports`): network / file / crypto / process-injection / registry.
   DLL/SYS also log exports (`E-exports`).
3. .NET (no traditional IAT) → use module/metadata/managed-reference summary as an
   equivalent anchor (see `dotnet-reverse`).
4. A "too clean" import table means dynamic loading is likely — mark it and move
   to dynamic API tracing.
5. Packed IAT rebuild failure → record `E-iat-repair-fail` and switch to dynamic
   API breakpoints; do not grind on the static IAT.

Until the import evidence (or a valid equivalent anchor / IAT-failure bypass) is
recorded, do **not** claim survey complete and do **not** draw deep conclusions.

## Setup notes (environment-specific)

- `idalib-mcp` exposes `idapro_*` tools over a Streamable-HTTP bridge; install from
  the project's GitHub repository, not the unrelated PyPI `ida-mcp`.
- Set `IDADIR` to your IDA install and run `ida-pro-mcp --install` to register the
  plugin; it listens locally (e.g. `127.0.0.1:13337`).
- Large / GUI samples can take minutes to auto-analyze — set a generous timeout
  and poll for readiness rather than assuming a hang.
- If a database file appears locked, close stale sessions and retry on a copy.

## Workflow

### Step 1 — Start the bridge (if using MCP)

Ensure the HTTP bridge is up before issuing tools. Prefer a background, hidden
start so analysis does not block the session.

### Step 2 — Open the binary

Open the sample (ideally a copy) in IDA / via the bridge. For large files, skip
auto-analysis and analyze on demand.

### Step 3 — Survey (with import gate)

Capture: architecture, entry point, interesting strings (URLs, paths, error
messages), and the **import categories** (MUST → evidence). Hot functions (high
xref count) are usually key logic.

### Step 4 — Deep key functions

Decompile / disassemble the target function; combine pseudocode + strings +
constants + callers/callees.

### Step 5 — Cross-references & data flow

Trace `xrefs_to` a string/address, build the call graph for a root, and trace
data flow forward/backward to follow a secret or decision.

### Step 6 — Annotate & rename

Continuously add comments and rename functions/variables as you understand them —
this raises the accuracy of later analysis and of any symbol migration.

### Step 7 — Report

Produce a report recording findings + reproducible steps (function names,
addresses, decompiled snippets).

## Prompt-engineering discipline

1. **Do not compute bases by hand** — use the bridge's integer-conversion tool.
2. **Survey first, then deep dive.**
3. **Annotate and rename as you go.**
4. **Follow cross-references** — find what references an interesting string/data.
5. **Pre-process obfuscation** — string decryption, import-hash removal,
   control-flow-flattening removal — before reasoning about logic.
6. **C++ STL** — identify library functions (FLIRT/Lumina) before analyzing
   business logic.
7. **Reason from disassembly**, not brute force.

## Tool catalog

The full `idapro_*` tool surface (survey, decompile, xrefs, data flow, search,
memory, patch, types, stack, signatures, sessions) is catalogued in
`references/tool-index.md`. Load it only when wiring or using the bridge.

## Quality bar

A defensible IDA pass records imports as evidence, surveys before diving, follows
cross-references, annotates findings, and leaves a reproducible report another
analyst can extend.

---

