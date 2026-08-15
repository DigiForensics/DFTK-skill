# Changelog

## Unreleased

- Documented DFTK's chain-of-custody audit ledger: `references/direct-cli.md` gains a section on `--audit` / `DFTK_AUDIT_LOG`, and SKILL.md §13 points to it for examinations that need a defensible record of what was executed. Requires a DFTK build that provides the ledger (post-3.2.1); the guidance is inert on older releases.

## 3.2.1

- Aligned the skill version with DFTK 3.2.1; skill content is unchanged from 3.2.0 (same `dftk prepare` / toolchain guidance, references, examples, and templates).

## 3.2.0

- Aligned the skill version with DFTK 3.2.0; added `references/toolchain.md` and SKILL.md §1 guidance describing `dftk prepare` so recipients can register an extracted forensic toolkit without manual PATH edits.

## 3.1.1

- Aligned the skill version with DFTK 3.1.1; skill content is unchanged from 3.1.0 (same investigation methodology, references, examples and templates).

## 3.1.0

- Expanded the standalone skill from a single-file usage guide into a progressive-disclosure investigation skill.
- Added claim-pattern, evidence-model, correlation, verification, negative-finding, reporting, and tool-selection guidance.
- Added domain references for artifact, Android/mobile, Linux, Windows, network, database, browser, web, email, disk, and timeline evidence.
- Added native DFTK MCP usage while retaining direct CLI fallback.
- Kept all reasoning guidance independent of challenge-specific scripts or a separate autonomous Agent runtime.
- Added reusable examples and reporting templates.
