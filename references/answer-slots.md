---
title: answer_slots.json — machine-readable answer sheet
summary: Format spec for answers/answer_slots.json used by the question workspace template.
read_when:
  - Filling answers/answer_slots.json for a multi-question forensic task
  - Defining the answer schema for scoring / automation
---

# answer_slots.json

A **machine-readable answer sheet** for competition-style or multi-question forensic
tasks. It complements `templates/answer-card.md` (the human-readable finding card).
The DFTK skill expects this file at `answers/answer_slots.json` inside a question
workspace (see `templates/question-workspace/`).

## Location

`answers/answer_slots.json` — relative to the question workspace root.

## Top level

A JSON object keyed by question id. Keep the original question numbering
(`Q1`, `Q2`, …) and preserve the exact asked wording in `question`.

```json
{
  "Q1": { "...": "..." },
  "Q2": { "...": "..." }
}
```

## Per-slot fields

- `question` *(string, required)* — the original question text, verbatim.
- `status` *(string, required)* — reasoning label. Use the **UPPER-CASE** values from
  SKILL.md §10, do not invent new ones:
  - `VERIFIED` — directly supported by sufficient source-traceable evidence, or a
    complete chain with no material unresolved link.
  - `SUPPORTED` — strongly supported, but one material verification step is
    unavailable/indirect; state it in `need_verify`.
  - `CANDIDATE` — a plausible lead exists but it is not sufficient as fact.
  - `UNRESOLVED` — available evidence/capabilities do not support a defensible answer.
  - `UNSUPPORTED` — the needed parser/capability is unavailable in this environment;
    explain the limitation in `need_verify`.
- `answer` *(any, required)* — the value, or `null` when not yet resolved. Keep it the
  exact expected type (string for a package name, URL for a URL, integer for a count).
- `evidence` *(array, optional but preferred for VERIFIED/SUPPORTED)* — each item is a
  provenance record:
  - `path` *(string)* — relative path inside the workspace (prefer `evidence/...` or
    `work/...` outputs). Never an absolute host path.
  - `locator` *(string, optional)* — precise location inside the file, e.g.
    `manifest/@package`, `table users.row 3.col login_ip`.
  - `field` *(string, optional)* — the key/attribute read.
  - `value` *(any, optional)* — the observed value at that locator.
  - `command` *(string, optional)* — the exact command used to reproduce, e.g.
    `aapt dump badging evidence/apk/sample.apk` or
    `dftk run apk_manifest --params '{"apk":"evidence/apk/sample.apk"}'`.
  - `method` *(string, optional)* — parser/tool name.
  - `hash` *(string, optional)* — `source_sha256` when available.
- `need_verify` *(string, optional)* — what is still required to upgrade `status`.
  Required when `status` is not `VERIFIED`.
- `notes` *(string, optional)* — short caveat / interpretation boundary.

## Rules

- Never invent a `path`, `locator`, `value`, `command`, or `hash` that was not
  actually produced. This is the same honesty rule as SKILL.md §7.
- `evidence[].path` is relative to the workspace root, not an absolute host path.
- If the question is about absence / non-occurrence, set `status` honestly
  (`UNRESOLVED` / `UNSUPPORTED`) and cite the search coverage in `need_verify` —
  absence of a hit is not proof of absence (SKILL.md §9, §11).
- Keep exact answers out of prose; the grader / downstream tool reads this file.

## Self-check

Run the bundled validator after editing:

```bash
python tools/validate_answers.py answers/answer_slots.json
```

It checks: valid JSON, required fields present, `status` in the SKILL.md §10 enum,
`VERIFIED` carries non-empty `evidence`, and (when present) that `evidence[].path`
exists in the workspace.

## Relationship to answer-card.md

`answer-card.md` is the examiner-facing conclusion card (narrative + confidence +
provenance). `answer_slots.json` is the machine-readable slot sheet for scoring /
automation. Produce both: the card for humans, the slots for tooling.
