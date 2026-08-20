---
name: digital-forensics
description: Authorized digital forensics and incident-response triage — memory dumps, disk/E01 timelines, PCAP溯源, host artifacts, and evidence preservation. Use for lawful investigations that require chain-of-custody, Volatility/Plaso timelines, Windows host artifacts, or IR evidence handling. Pairs with DFTK for local file/artifact parsing and with the DFTK 3.4.0 audit ledger for process provenance.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - dfir
  - incident-response
  - memory
  - timeline
  - pcap
  - host-artifacts
---

# Digital Forensics & Incident Response Triage

This skill teaches an Agent how to perform **defensive, read-only digital forensics and IR triage**. It covers the evidence classes a DFTK local-file parser does not reach on its own: volatile memory, full-disk/E01 super-timelines, live PCAP溯源, and Windows host artifacts (Prefetch, Shimcache, Event Logs, browser history).

It is a **methodology skill**, not a parser. The executing capabilities are external forensic tools (Volatility 3, Plaso, tshark, Eric Zimmerman tools, Autopsy/FTK Imager). DFTK remains the layer of choice for the file-level artifacts it already parses (APK, SQLite, PCAP, browser, email, hashes, strings, archives); this skill handles the *system-level* acquisition and timeline work and feeds findings into DFTK where a specific artifact is extractable.

## Relationship to DFTK

- For a **local file or disk image artifact** (APK, PCAP, SQLite, registry, E01, browser export), use `dftk`. Its 71 read-only tools return structured Observation/Evidence results and can run under MCP server policy.
- When the task is **memory/disk timeline, host-artifact reconstruction, or IR preservation**, use this skill.
- Both share the same reasoning contract: claim → evidence requirement → capability → bounded execution → verification. When you run any command here, enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) so the *process* is recorded with evidence hashes — this is the chain-of-custody record.

## Operating contract (read-only, preserve, prove)

1. **Work on copies.** Acquire a verified image; never analyze the original. Compute and record SHA-256 of every artifact before touching it.
2. **Record provenance.** For each conclusion: source (file/command), locator (path/offset/row), value, method/hash.
3. **Preserve chain of custody.** Note acquisition command, time zone, and analyst in the timeline.
4. **Separate fact from inference.** Use VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED / UNSUPPORTED.
5. **Declassify/redact IOCs by sensitivity** before any shared report.

## 1. Acquisition & preservation

```text
□ Compute SHA-256 of the source; store the original read-only.
□ Record acquisition tool, command, and time zone (UTC offset).
□ Work only on a verified copy; never mutate the original in place.
□ Note chain-of-custody metadata in the case timeline.
```

For memory: capture a full RAM dump from a trusted agent (e.g. `winpmem`, `AVML` on Linux, `osxpmem` on macOS) before any live analysis. For disk: image with `dc3dd`/`FTK Imager`/ `dd` + `sha256` and verify.

## 2. Memory analysis (Volatility 3)

```bash
vol -f mem.dmp windows.info          # profile / OS build
vol -f mem.dmp windows.pslist         # processes
vol -f mem.dmp windows.netscan       # network connections
vol -f mem.dmp windows.cmdline        # command lines
vol -f mem.dmp windows.malfind        # injected/unmapped regions
```

Map suspicious processes to host artifacts and to any C2 in the PCAP before asserting attribution.

## 3. Host artifacts (Windows)

```text
□ Event logs: Security / PowerShell / Sysmon (Operational + Microsoft-Windows-Sysmon/Operational)
□ Persistence: Run/RunOnce keys, services, scheduled tasks, WMI EventSubscription, startup folders
□ Execution traces: Amcache, Prefetch, Shimcache, BAM, RecentFileCache, UserAssist
□ Browser: history, cookies, downloads, login URLs (feed to DFTK browser parsers)
□ Registry: mounted USB (USBSTOR/USBKEYS), RDP (TERMSRV), last logged-on user
```

Use Eric Zimmerman's `RECmd`/`PECmd`/`MFTECmd` for parsed timelines; cross-reference with the super-timeline below.

## 4. Super-timeline (Plaso / log2timeline)

```bash
log2timeline.py --storage-file case.plaso evidence/        # build
psort.py -o l2tcsv case.plaso > timeline.csv               # export
psort.py -o json case.plaso > timeline.json               # for tooling
```

Fuse memory, host, and (if present) DFTK-parsed artifacts into one chronological spine. Prefer a single timeline over scattered notes.

## 5. Network (PCAP溯源)

```bash
tshark -r capture.pcap -q -z conv,tcp            # session summary
tshark -r capture.pcap -z dns,tree                # DNS tree
tshark -r capture.pcap -Y http.request -T fields -e http.host -e http.request.uri
```

Export suspicious streams to `protocol-reverse/` for frame/state-machine recovery, or to `malware-analysis/` when a C2 pattern emerges.

## 6. Reporting & handoff

- Use `templates/case-report.md` for the case write-up (reuse DFTK-skill's claim-card format).
- Declassify IOCs: mark infrastructure, hashes, and hosts by sensitivity tier.
- Before handoff, run a case-review pass: every Finding must cite an existing Evidence record; every Evidence must carry a reproducible command + hash.

## 7. Domain references — load only when needed

- triage checklist and acquisition order → `references/forensics-triage.md`
- memory → Volatility 3 plugin map
- host → Zimmerman tooling + registry keys
- related: `../malware-analysis/`, `../threat-hunting/`, `../protocol-reverse/`, `../server-forensics/`
- run these steps under the DFTK MCP server (preferred) → `../../references/mcp-setup.md`; worked MCP+CLI calls → `examples/memory-triage.md`

## 8. Quality bar

A complete DFIR pass answers the claim with the smallest reproducible evidence chain, preserves provenance and chain of custody, distinguishes fact from inference, redacts by sensitivity, and leaves results re-examinable by another analyst.

---

