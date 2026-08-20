---
name: case-orchestrator
description: Coordinate a multi-step, evidence-preserving digital-forensics case. Use it to route work to specialist skills and keep DFTK observations in one CaseSession.
version: 3.4.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags: [orchestration, workflow, case-management, forensics, triage, mcp]
---

# Case Orchestrator

Use this skill for an investigation that spans multiple artifacts, questions, or
specialist domains. It coordinates the work; domain skills provide the procedures.

## Workflow

1. Define the case scope and the claims that need evidence.
2. Create a case with `dftk_case(action="new", name="<case>")`.
3. For a mixed or unfamiliar evidence set, run `evidence.intake` first and record
   it in the Case. Inspect its `next_steps`; they are a triage plan, not findings.
4. Use `dftk_search_capabilities` and `dftk_describe` to select a capability for the
   current evidence gap.
5. Run it with `dftk_run(..., case_id="<case_id>")`.
6. Check the result before using it. `ok: true` means `status` is `ok` or `partial`;
   otherwise inspect `observation.status` and `observation.errors`.
7. Read large persisted results with `dftk_read_case_run`, then use
   `dftk_case(action="timeline"|"export", case_id="<case_id>")` for correlation and
   handoff.

After each material step, call `dftk_case(action="next", case_id="<case_id>")`.
It returns a compact queue derived from the persisted intake and Case state, rather
than requiring the Agent to rediscover every tool. It may recommend `graph` and
`timeline`; these are correlation views, not additional evidence collection.

For the first response, prefer `dftk_case(action="guided_intake", ...)` over the
standalone Recipe. It writes the intake and every selected child run separately,
which preserves recovery and paging after an Agent context reset.

On a resumed Case, call `dftk_case(action="brief", case_id="<case_id>")` first.
It is the compact handoff surface; page a referenced run before relying on its
highlights.

Use the generated `case_id` returned by `new` for `show`, `timeline`, and `export`.
`dftk_describe` takes a DFTK capability name, not an MCP tool name.

## Routing

| Case type | Start with |
|---|---|
| Android or iOS artifacts | `mobile-reverse`, `apk`, `apk-reverse`, `digital-forensics` |
| Windows or Linux intrusion | `digital-forensics`, `server-forensics`, `threat-hunting` |
| Phishing and email | `email-security`, `digital-forensics` |
| Network captures or custom protocols | `pcap`, `protocol-reverse` |
| Executables or malware | `reverse-exe`, `reverse-engineering`, `malware-analysis` |
| Desktop clients or extensions | `thick-client`, `browser-extension-reverse` |
| Saved web configuration or access logs | `web-forensics` |
| Source, identity, database, OT, or supply chain | matching specialist skill |

## Case record

- Keep every DFTK run for the case under the same `case_id`.
- Separate tool facts from analyst inference and note coverage limits.
- Use the server policy as launched; do not bypass a blocked operation with a broader
  tool or a different evidence root.
- Export the case when handing it to another analyst or producing a report.

## References

- [MCP setup and result contract](../../references/mcp-setup.md)
- [Skill router](../../references/skill-router.md)
- [Domain playbooks](references/playbooks.md)
- [Worked engagement](examples/worked-engagement.md)
- [CLI fallback](../../references/direct-cli.md)
