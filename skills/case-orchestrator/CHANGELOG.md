# Changelog

## 3.3.0 (2026-08-16)
- New orchestration skill: composes the 29 specialist sub-skills into end-to-end,
  evidence-preserving engagements.
- Encodes the verified DFTK 3.3.0 MCP tool loop (case → search → describe → run →
  read → handoff) with authoritative argument names confirmed by a live stdio handshake.
- Documents the two non-obvious contract rules: `dftk_describe` takes a *capability* name
  (not an MCP tool name); `dftk_case` `show`/`timeline`/`export` need the *generated*
  `case_id`, not the friendly `name`.
- Adds `references/playbooks.md` (8 scenario playbooks) and
  `examples/worked-engagement.md` (verified Android triage transcript).
