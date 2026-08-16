# Thick client triage cheatsheet

Command and tool reference for `thick-client`. Authorized scope only — review apps
you own or are authorized to assess; do not bypass third-party license / integrity
checks you are not cleared to test. `dftk hash` the installer first.

## Draw the trust boundary

```bash
# Windows
powershell -c "Get-Process | Select Name,Path,Id"     # process tree
netstat -ano | findstr LISTENING                       # listening ports
# macOS / Linux
lsof -i -P -n | grep LISTEN
ps aux | grep -i target
```

Record: child processes, drivers/services, listening ports, outbound domains,
sensitive local paths (`%APPDATA%`, Keychain, registry).

## Local attack surface

```text
□ Plaintext config / hardcoded keys / debug switches in the install dir
□ DLL search-order / hijack (Windows) — procmon "PATH" + LOAD_WITH_ALTERED_SEARCH_PATH
□ SQLite / local DB files — permissions + encryption-at-rest
□ IPC channel — who can connect? authenticated? (named pipe / Unix socket / COM)
□ Electron: asar extract → bundle review (hand JS to js-reverse)
```

## Network surface

```text
□ System proxy / app-specific TLS settings
□ Certificate pinning → pair with mobile/js methods or Frida
□ Hidden admin / privileged API the client can reach
```

## Per-platform tool chain

| Platform | Tools |
|----------|-------|
| Windows | Process Monitor, API Monitor, dnSpy, IDA/Ghidra, Sysinternals, Burp/mitmproxy |
| macOS | `fs_usage`, `log stream`, `otool`, Frida/lldb, Hopper |
| Linux | `strace`/`ltrace`, `lsof`, `gdb`/Frida, Wireshark |
| Electron | `asar extract`, `nexe`/`pkg` detection, js-reverse |

## Reverse-verify routing

```text
□ .NET     → dotnet-reverse
□ native   → ida-reverse / ghidra-reverse
□ Electron → asar + js-reverse
□ protocol → protocol-reverse
□ update / supply-chain → supply-chain-security
```

## Cross-links
- DFTK MCP: `../../../references/mcp-setup.md`.
- .NET: `../../dotnet-reverse/`, native: `../../ida-reverse/`, JS: `../../js-reverse/`.
- Protocol: `../../protocol-reverse/`, supply chain: `../../supply-chain-security/`.
