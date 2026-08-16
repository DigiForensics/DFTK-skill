# case-orchestrator

The engagement-lead skill for DFTK-skill: turns a forensic goal into a defensible,
evidence-preserving workflow. It composes the specialist sub-skills and executes them
through the verified DFTK MCP tool loop — `dftk_case` → `dftk_search_capabilities` →
`dftk_describe` → `dftk_run` → `dftk_read_case_run` → `dftk_case` handoff.

See `SKILL.md` for the loop and `references/playbooks.md` for per-engagement steps
(mobile, host, email, network, web/thick-client, malware, supply-chain, identity). A
verified transcript lives in `examples/worked-engagement.md`.
