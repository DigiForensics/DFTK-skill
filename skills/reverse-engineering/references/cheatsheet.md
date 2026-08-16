# Reverse-engineering tool-selection cheatsheet

Pick the module that matches the artifact and the depth you need. All modules are
read-only / evidence-preserving and pair with DFTK's case + audit-ledger model.

| If the target is… | Use | When |
|-------------------|-----|------|
| A generic native binary / CLI | `radare2` | Fast survey, scripting, cross-platform, no license cost. |
| A complex native binary needing best-in-class decompilation | `ida-reverse` | Deep control-flow, FLIRT/type recovery, `idalib-mcp` for agentic workflows. |
| Open-source RE / batch headless | `ghidra-reverse` | Collaborative projects, Ghidra Server, optional `ghidra-mcp` bridge. |
| A stripped Go / Rust binary | `go-rust-reverse` | Recover function names (GoReSym / golang_loader_assist / rust- demangle). |
| A .NET / C# assembly | `dotnet-reverse` | IL-first; dnSpyEx / de4dot for deobfuscation. |
| An Android APK | `apk-reverse` (tool method) + `apk` (read-only playbook) | Decompile, review, rebuild; keep the authorized-forensics framing. |
| An iOS app / Mach-O / ObjC / Swift | `macos-reverse` + `mobile-reverse` | Mach-O structure, Objective-C/Swift symbol recovery. |
| A browser extension (crx / xpi) | `browser-extension-reverse` | Unpack manifest + content/script review. |
| A desktop thick client (C/S) | `thick-client` | Protocol + client logic review. |
| A web front-end bundle | `js-reverse` | Beautify / de-obfuscate / reconstruct build. |
| Two builds of the same binary | `binary-diff` | LLM-assisted cross-version symbol/behavior migration. |
| Unknown binary protocol / PCAP | `protocol-reverse` | Struct recovery, Protobuf/Thrift decode. |

## Decision rules

- **Don't guess the decompiler by habit.** Survey first (`radare2` or `ida-reverse`
  `idapro_survey_binary`), then commit to the deep tool only if the survey justifies it.
- **Obfuscation first.** For .NET and JS, run deobfuscation *before* you read logic;
  reading obfuscated IL/JS wastes effort.
- **Stripped Go/Rust is not "no symbols"** — `go-rust-reverse` usually recovers most
  function names automatically; try it before manual renaming.
- **Diff before deep RE.** If you already have a known-good build, `binary-diff` turns
  a 4-hour manual rename into a review of the *changed* set.
- **Mobile = two passes.** Static (`apk-reverse` / `mobile-reverse`) then runtime
  review (Frida/Objection) — but only in an authorized, isolated environment.

## Cross-links
- DFTK MCP: `../../../references/mcp-setup.md` (run these tools under server policy).
- Capability discovery: `dftk_search_capabilities` / `dftk_describe`.
- Reasoning contract: `anti-analysis.md`, `languages-compiled.md`.
