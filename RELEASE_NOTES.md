# DFTK Skill 3.3.0

The standalone Agent Skill for [DigiForensics/DFTK](https://github.com/DigiForensics/DFTK).

This release aligns the skill with **DFTK 3.3.0** and is a substantial capability
release, not a version-number bump. It adds first-class support for the DFTK native
MCP server, a verified catalog of all 72 capabilities, a case-orchestrator layer,
and 30 progressive-disclosure sub-skills — while keeping the original
investigation methodology, `references/` playbooks, `examples/`, and `templates/`.

## What's new in 3.3.0

- **Native DFTK MCP server integration.** `references/mcp-setup.md` documents how to
  launch the server (`dftk mcp --root <evidence_dir>`) and wire it into any MCP host
  over stdio — WorkBuddy, Claude Desktop, Cursor, or anything else that can launch a
  stdio server. The server exposes six tools — `dftk_doctor`,
  `dftk_search_capabilities`, `dftk_describe`, `dftk_run`, `dftk_case`,
  `dftk_read_case_run` — and **owns** the safety / root / network / timeout / audit
  policy so a client cannot weaken it. A `mcp-config.example.json` is included.
- **Honest result contract (server-side fix).** `dftk_run` / `dftk_case` now return a
  top-level `ok` that mirrors `observation.status` (`ok` / `partial` → `true`;
  `unsupported` / `error` / `blocked` → `false`). A client that branches on `ok` will
  no longer mistake a failed run for success. This requires DFTK 3.3.0 or later — the
  fix lives in the server, not the docs.
- **Verified capability catalog.** `references/capabilities.md` is an authoritative,
  auto-extracted catalog of all **72 DFTK 3.3.0 capabilities** across 20 domains
  (name / safety / parameters / external-tool `requires`), cross-checked against the
  live registry. It is the source of truth for `dftk_describe` / `dftk_run` names.
- **Case orchestrator (30th sub-skill).** `skills/case-orchestrator/` composes the
  specialists into a defensible, evidence-preserving workflow driven by the verified
  MCP tool loop: `dftk_case` → `dftk_search_capabilities` → `dftk_describe` →
  `dftk_run` → `dftk_read_case_run` → `dftk_case`.
- **30 domain sub-skills** (progressive disclosure) covering reverse-engineering and
  forensics: `apk`, `apk-reverse`, `binary-diff`, `browser-extension-reverse`,
  `case-orchestrator`, `case-review`, `code-audit`, `database-security`,
  `digital-forensics`, `dotnet-reverse`, `email-security`, `firmware-forensics`,
  `ghidra-reverse`, `go-rust-reverse`, `ida-reverse`, `identity-federation`,
  `js-reverse`, `macos-reverse`, `malware-analysis`, `mobile-reverse`, `ot-ics`,
  `pcap`, `protocol-reverse`, `radare2`, `reverse-engineering`, `reverse-exe`,
  `server-forensics`, `supply-chain-security`, `threat-hunting`, `thick-client`.
- **Chain-of-custody audit ledger guidance.** `references/direct-cli.md` documents
  `--audit` / `DFTK_AUDIT_LOG` for examinations that need a defensible record of what
  was executed (requires DFTK 3.3.0+; inert on older releases).
- **Client-agnostic, MCP-first.** Documentation is written for the stdio MCP server and
  works with any compliant host; the DFTK CLI is documented as a fallback when MCP is
  unavailable.

## What this skill is

DFTK Skill turns the original single-file tool-use guidance into a complete but
progressively loaded forensic investigation skill. The main `SKILL.md` stays focused
on invariant reasoning and safety rules; detailed claim/evidence/domain guidance lives
under `references/`, and worked examples under `examples/` and `skills/*/examples/`.

## Architecture (since 3.1.0)

- **Progressive disclosure**: `SKILL.md` (reasoning + safety) loads `references/`,
  `examples/`, `templates/` and `skills/*` on demand.
- **No longer bundled in the wheel**: the skill no longer ships inside the `dftk` PyPI
  package. `dftk skill --install` fetches the matching tag (`v{TOOLKIT_VERSION}`)
  directly from this GitHub repository, so the skill text and the toolkit version stay
  in lockstep.
- **Domain sub-skills** under `skills/` (30 in 3.3.0).

## Scope

Designed to work with DFTK 3.3 native MCP or the existing DFTK CLI. It deliberately
does not implement an Agent runtime, case-question state machine, or
challenge-specific solver. The skill does not reimplement forensics — it composes
DFTK's read-only / evidence-preserving / chain-of-custody contract.
