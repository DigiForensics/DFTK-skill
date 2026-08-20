# Skill Router — pick the right module

DFTK-skill ships progressive-disclosure sub-skills under `skills/`. The generated
[specialist skill catalog](skills.md) lists every available module. Choose the module
that matches the task; when several apply, begin with an umbrella skill such as
`reverse-engineering` or `digital-forensics`, then move to the specialist module.

**Multi-step engagement:** start with `skills/case-orchestrator/`. It routes the work to relevant sub-skills and keeps DFTK runs in one CaseSession.

`capabilities.md` lists all 79 DFTK 3.4.0 capabilities, including names, safety levels, parameters, and external-tool requirements. Use it to identify the exact name for `dftk_describe` or `dftk_run`.

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
| Investigate saved web configuration or access logs | `web-forensics/` |
| General RE methodology / where to start | `reverse-engineering/` |

## By discipline

| Discipline | Modules |
|---|---|
| **Reverse engineering** | `reverse-engineering/`, `radare2/`, `ida-reverse/`, `ghidra-reverse/`, `dotnet-reverse/`, `go-rust-reverse/`, `macos-reverse/`, `browser-extension-reverse/`, `thick-client/`, `binary-diff/`, `reverse-exe/`, `apk-reverse/`, `apk/`, `mobile-reverse/`, `js-reverse/`, `protocol-reverse/`, `pcap/` |
| **Digital forensics & IR** | `digital-forensics/`, `firmware-forensics/`, `server-forensics/`, `web-forensics/` |
| **Malware & detection** | `malware-analysis/`, `threat-hunting/` |
| **Code & supply chain** | `code-audit/`, `supply-chain-security/` |
| **Defensive security review** | `email-security/`, `identity-federation/`, `database-security/`, `ot-ics/` |
| **Case & evidence** | `case-review/` |

## Sequencing patterns

- **Malware sample in hand** → `malware-analysis/` → IOCs feed `threat-hunting/` (detections) and `digital-forensics/` (lateral spread).
- **Suspicious app** → `apk/` or `mobile-reverse/` (static) → `apk-reverse/`/`mobile-reverse/` (dynamic) → `reverse-engineering/` for method.
- **Unknown protocol** → `pcap/` (capture) → `protocol-reverse/` (recover structure).
- **Source available** → `code-audit/` (first-party) + `supply-chain-security/` (dependencies/pipelines).
- **Saved web root or access logs** → `web-forensics/` → `server-forensics/` only when live-host evidence is needed.
- **Any local tooling run** → enable DFTK 3.4.0 `--audit` / `DFTK_AUDIT_LOG` so the pass is reproducible; `case-review/` for the evidence graph.

## MCP-first workflow

When the host exposes `dftk_*` tools, use them for DFTK operations: the server
enforces safety, root, and network policy. A typical sequence is:

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
