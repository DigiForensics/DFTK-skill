# DFTK Skill 3.4.0

This release aligns the Skill with **DFTK 3.4.0** and makes the runtime repository
the only recommended entry point for Agent installations.

## What changed

- **Agent bootstrap.** `dftk agent setup --root … --workspace … --install-skill`
  installs this version-matched bundle and creates a reviewable MCP configuration
  artifact. It emits portable JSON plus a Codex TOML fragment; it does not overwrite
  a host's existing global configuration.
- **Recoverable investigation loop.** Guidance now starts Cases with
  `guided_intake`, uses `next` for a deterministic work queue, `brief` for bounded
  context recovery, and `graph` to correlate source-linked entities before handoff.
- **Expanded DFTK catalog.** The generated capability reference covers 79 tools,
  including evidence intake, EVTX hunting, fixed-profile SSH snapshots, YARA scans,
  and static web-shell leads.
- **Clear ownership.** DFTK provides the runtime and local MCP server; this
  repository provides the complete Skill bundle, references, templates, and
  specialist guidance. Do not install only `SKILL.md`.

## Safe installation

```bash
python -m pip install --upgrade "dftk[mcp]"
dftk agent setup \
  --root /read-only/evidence \
  --workspace /writable/case \
  --install-skill \
  --config-out /writable/case/dftk-agent-config.json
```

Import the generated MCP fragment through the host's normal approval flow, verify
with `dftk mcp --root … --workspace … --check`, and start a new Agent session.
