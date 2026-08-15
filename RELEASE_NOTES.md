# DFTK Skill 3.2.1

The standalone Agent Skill for [DigiForensics/DFTK](https://github.com/DigiForensics/DFTK).

This release aligns the skill with **DFTK 3.2.1**. Skill content is functionally unchanged from 3.2.0 — same investigation methodology, `references/` playbooks, `examples/`, and `templates/`.

## What this skill is

DFTK Skill turns the original single-file tool-use guidance into a complete but progressively loaded forensic investigation skill. The main `SKILL.md` stays focused on invariant reasoning and safety rules; detailed claim/evidence/domain guidance lives under `references/`.

## Architecture (since 3.1.0)

- **Progressive disclosure**: `SKILL.md` (reasoning + safety) loads `references/`, `examples/`, `templates/` on demand.
- **No longer bundled in the wheel**: the skill no longer ships inside the `dftk` PyPI package. `dftk skill --install` fetches the matching tag (`v{TOOLKIT_VERSION}`) directly from this GitHub repository, so the skill text and the toolkit version stay in lockstep.
- **Domain sub-skills** under `skills/`: `apk`, `pcap`, `reverse-exe`, `server-forensics`.

## Scope

Designed to work with DFTK 3.2 native MCP or the existing DFTK CLI. It deliberately does not implement an Agent runtime, case-question state machine, or challenge-specific solver.
