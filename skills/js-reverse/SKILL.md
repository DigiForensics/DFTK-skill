---
name: js-reverse
description: >-
  Front-end JavaScript reverse engineering — locating signing/encryption parameter
  chains, observing request flows, sampling runtime values, and reconstructing the
  logic locally for evidence-based reproduction. Read-only-first, evidence-first.
  Use for authorized analysis of endpoints you own or are authorized to assess.
  For browser extensions use browser-extension-reverse; for binaries use
  ida-reverse / radare2.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - javascript
  - web
  - forensics
---

# Front-end JS reverse engineering

Methodology for analyzing client-side JavaScript: locating where a request's
signature / encryption parameter is produced, observing the page's request chain
and script sources, sampling function arguments/returns at runtime, and
reconstructing the logic locally (Node) for a reproducible, evidence-based
result.

This is a **methodology skill**. Concrete tooling (browser automation, CDP, hook
framework) is external; nothing here is bundled in the `dftk` wheel. When the
evidence is a captured PCAP or a saved script file, prefer `dftk` for structured
Observation/Evidence output.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working
  so the analysis process is recorded with evidence hashes.
- `dftk hash` is the DFIR-preferred hashing for any saved script/artifact.
- Hand off protocol/state-machine recovery to `protocol-reverse` once you have the
  raw bytes; hand off obfuscated control flow to the AST/deobfuscation notes
  (below). For browser extensions, use `browser-extension-reverse`.

## Operating contract (observe, capture, evidence)

1. **Authorized scope only.** Analyze endpoints you own or are explicitly
   authorized to assess. Do not bypass access controls you are not authorized to
   test.
2. **Observe before guessing.** Never fabricate a browser/`window`/`document`
   shim. Build the local environment strictly from observed page evidence.
3. **Evidence-first.** Every conclusion cites the script URL, function, and the
   observed value (or the recorded request that produced it).
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
5. **Preserve provenance.** Record each step (script source, breakpoint, sample)
   so another analyst can reproduce.

## Five-phase workflow

### 1. Observe

Confirm the target request, related scripts, and candidate functions — without
guessing the environment.

- Open the target page; list network requests and find the target request.
- Trace the request's initiator (call stack / initiator script).
- Enumerate loaded scripts and search sources for signature/encrypt keywords.

Produce: target request URL or signature, initiator线索, suspicious script URLs,
and an initial task record.

### 2. Capture

Take minimal-intrusion samples of the target request: argument examples, call
order, runtime evidence.

- Prefer request-breakpoint / runtime-evaluate for light observation.
- On hit, read the paused context first.
- Use text breakpoints only when needed.

### 3. Rebuild

Organize page evidence into locally iterable Node reproduction material.

- The local environment MUST be built from observed page evidence.
- Never invent `window` / `document` / `navigator` / `crypto` / `storage` shims.
- Record one minimal causal patch decision at a time.

### 4. Patch (local environment)

Drive the local rebuild by errors and first divergence until the script stably
produces the target parameter.

- See what is missing, then supply it.
- One minimal patch decision per step; re-test immediately after each.
- Log every patch in the task record.

### 5. DeepDive

Once the local script runs, optionally do deobfuscation, control-flow recovery,
and business-logic distillation.

- If the task is only to produce the signature, this phase may be downgraded.
- If the algorithm chain will be reused long-term, this phase is required.
- Note anti-debug techniques (debugger statements, timer traps) as findings, not
  as things to defeat on someone else's property.

## Execution requirements

- Write every important step into a local task artifact.
- If you cannot explain why a tool/step is called, do not call it.
- Prefer existing runtime/hook capabilities for取证 directly; do not reimplement
  them as ad-hoc scripts.
- On failure, fall back to a smaller, observation-only pass.

## Domain references — load only when needed

- local reproduction / environment rebuild → `references/env-rebuild.md`
- AST deobfuscation notes → `references/ast-deobf.md`
- related: `protocol-reverse` (raw bytes), `browser-extension-reverse` (extensions)

## Quality bar

A defensible JS-reverse pass observes before guessing, builds the local
environment only from page evidence, records provenance for every step, and
separates fact from inference — leaving a reproducible Node reproduction another
analyst can run.

---

