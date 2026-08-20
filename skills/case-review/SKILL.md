---
name: case-review
description: Read-only review of a forensics/reverse-engineering case package before report handoff — verifies scope readiness, Evidence→Finding→Path traceability, work-item and timeline coverage, and artifact hash integrity. Use to make a case defensible before it leaves your hands.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - dfir
  - case-review
  - quality
  - chain-of-custody
  - audit
---

# Evidence Graph Review

A read-only quality gate for a case package before report handoff. It audits an existing `work/<case>/` directory without changing the case or touching any target. The point is defensibility: every Finding traces to Evidence, every Evidence is reproducible, and the chain of custody holds.

This skill is the natural companion to the DFTK 3.4.0 audit ledger (`--audit` / `DFTK_AUDIT_LOG`): the ledger records *process* (what commands ran, with evidence hashes); this skill validates *structure* (does the report hold together).

## Scope

Covers:
- Scope metadata and target-activity readiness.
- Evidence record structure and reproducibility fields.
- References from work items and timeline entries back to Evidence.
- Structured Findings and Paths in the report.
- Optional SHA-256 verification for case-local artifacts.

MUST NOT perform reconnaissance, exploitation, dynamic instrumentation, or target changes. Those belong to the analysis skill that produced the case.

## Operating contract

- Read-only: never mutate the case or the evidence.
- Confirm the case path and choose review mode.
- Resolve every error before claiming a handoff is complete.

## Workflow

### Phase 1 — Intake
Confirm these exist in `work/<case>/`:
```text
□ scope.md      — authorization, scope, network_profile
□ timeline.md   — chronological events with sources
□ workitems.md  — task list with status
□ evidence/     — artifacts + per-artifact hash/manifest
□ report/       — draft findings (claim-card / case-report)
```

### Phase 2 — Traceability
For each Finding, verify:
```text
□ Finding references at least one existing Evidence id.
□ Evidence id exists and is reproducible (command + hash recorded).
□ Path steps (if any) carry an allowed path_type and an Evidence reference.
□ Work items / timeline entries point to known Evidence (no dangling refs).
□ Unlinked Evidence is explained, not silently dropped.
□ Confidence on validated Findings is stated.
```

### Phase 3 — Fixity (hash integrity)
When an Evidence record carries both `content_hash` and `artifact_path`:
```bash
sha256sum "evidence/<file>"        # must match the recorded content_hash
```
A mismatch is a hard failure — replace the corrupted working copy from the verified original before proceeding.

### Phase 4 — Handoff
Produce a review summary that states: pass/fail per check, list of gaps, and the strict-mode verdict. Attach it to the report. Only then is the case ready for handoff or further analysis.

## Next-step menu pattern
After each phase, present 3–6 numbered options (e.g. fix scope field / complete Evidence reproducibility / regenerate review summary / return to analysis / pause for human review). Do not advance across phases without user direction.

## Domain references
- review checklist → `templates/review-checklist.md`
- evidence model & claim-card format → DFTK-skill `../server-forensics/templates/claim-card.md`
- audit ledger (process provenance) → DFTK `../../references/direct-cli.md` and the DFTK 3.4.0 release notes

## Quality bar
A case passes review only when every Finding cites existing, reproducible Evidence; every Evidence carries a command + hash; timeline/workitems are linked; and hash integrity is verified or its omission explained. The review is not legal advice and does not replace organizational evidence-handling procedures.

---

