# Skill Router — pick the right module

DFTK-skill ships 29 progressive-disclosure sub-skills under `skills/`. Load the one that matches the task; if several apply, start from the umbrella (`reverse-engineering`, `digital-forensics`) and drill into the tool-specific module. Every module is read-only / evidence-preserving and ties back to the DFTK 3.3.0 audit ledger.

**Full engagement?** Start with `skills/case-orchestrator/` — it routes the goal to the right sub-skills below and runs them through the verified DFTK MCP loop, keeping every action in one CaseSession.

**What can DFTK actually do?** `capabilities.md` is the verified catalog of all 72 DFTK 3.3.0 capabilities (name, safety, params, external-tool requirements) — generated from the live registry. Use it to find the exact `name` for `dftk_describe` / `dftk_run` instead of guessing.

## By task

| You want to… | Use |
|---|---|
| Analyze a binary from the CLI (radare2/Cutter) | `radare2/` |
| Decompile with IDA Pro | `ida-reverse/` |
| Decompile open-source (Ghidra) | `ghidra-reverse/` |
| Reverse a .NET / C# assembly (dnSpyEx/de4dot) | `dotnet-reverse/` |
| Recover stripped Go / Rust symbols | `go-rust-reverse/` |
| Analyze a macOS / Mach-O / ObjC / Swift binary | `macos-reverse/` |
| Reverse a browser extension (crx/xpi) | `browser-extension-reverse/` |
| Review a desktop thick-client (C/S) app | `thick-client/` |
| Migrate symbols across two binary versions | `binary-diff/` |
| Only have a compiled Windows/Linux executable | `reverse-exe/` |
| Reverse an APK (jadx/apktool/frida) | `apk-reverse/` |
| Static APK forensic triage (no execution) | `apk/` |
| Reverse Android **or** iOS apps | `mobile-reverse/` |
| Reverse front-end JS / web bundles | `js-reverse/` |
| Recover a binary/Protobuf protocol or PCAP | `protocol-reverse/` |
| Analyze network captures (PCAP) | `pcap/` |
| General RE methodology / where to start | `reverse-engineering/` |

## By discipline

| Discipline | Modules |
|---|---|
| **Reverse engineering** | `reverse-engineering/`, `radare2/`, `ida-reverse/`, `ghidra-reverse/`, `dotnet-reverse/`, `go-rust-reverse/`, `macos-reverse/`, `browser-extension-reverse/`, `thick-client/`, `binary-diff/`, `reverse-exe/`, `apk-reverse/`, `apk/`, `mobile-reverse/`, `js-reverse/`, `protocol-reverse/`, `pcap/` |
| **Digital forensics & IR** | `digital-forensics/`, `firmware-forensics/`, `server-forensics/` |
| **Malware & detection** | `malware-analysis/`, `threat-hunting/` |
| **Code & supply chain** | `code-audit/`, `supply-chain-security/` |
| **Defensive security review** | `email-security/`, `identity-federation/`, `database-security/`, `ot-ics/` |
| **Case & evidence** | `case-review/` |

## Sequencing patterns

- **Malware sample in hand** → `malware-analysis/` → IOCs feed `threat-hunting/` (detections) and `digital-forensics/` (lateral spread).
- **Suspicious app** → `apk/` or `mobile-reverse/` (static) → `apk-reverse/`/`mobile-reverse/` (dynamic) → `reverse-engineering/` for method.
- **Unknown protocol** → `pcap/` (capture) → `protocol-reverse/` (recover structure).
- **Source available** → `code-audit/` (first-party) + `supply-chain-security/` (dependencies/pipelines).
- **Any local tooling run** → enable DFTK 3.3.0 `--audit` / `DFTK_AUDIT_LOG` so the pass is reproducible; `case-review/` for the evidence graph.

## MCP-first workflow

When the host Agent exposes the `dftk_*` tools, prefer them over raw shell — the
server enforces the safety / root / network policy. Typical sequence:

1. `dftk_doctor()` — confirm health + the policy you're bound by.
2. `dftk_search_capabilities(query=…)` — find the right capability (Chinese aliases
   work: 联系人, 短信, 通话, 流量, 注册表, 浏览器, 时间, 哈希, 邮件, …).
3. `dftk_describe(name)` — read its exact contract.
4. `dftk_run(name, params, case_id?)` — execute under server policy; persist into a
   case when you want an evidence graph.
5. `dftk_read_case_run(case_id, seq)` — page the persisted result *without* re-running.
6. `dftk_case(action, case_id)` — `timeline` / `export` for handoff.

### Skill ↔ MCP tool mapping

| You're working in… | Reach for this first |
|---|---|
| Any local extraction / triage | `dftk_search_capabilities` → `dftk_run` (persist to a case) |
| `malware-analysis` / `digital-forensics` | `dftk_run` per worked step, then `dftk_read_case_run` to page large output |
| `case-review` | `dftk_case(action="show"|"timeline")` to inspect the evidence graph |
| `reverse-engineering` tool selection | `dftk_search_capabilities` / `dftk_describe` to confirm what a capability needs |
| Pre-flight sanity | `dftk_doctor` (also reports which external binaries are present) |

Full launch command, six-tool contract, and the WorkBuddy `mcp.json` snippet:
`mcp-setup.md`.
