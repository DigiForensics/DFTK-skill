# Forensics Triage Checklist

Use this as the first-pass order of operations for any authorized DFIR case.

## 0. Before you touch anything
- [ ] Confirm authorization scope (who, what systems, what time window).
- [ ] Identify the evidence type: memory, disk image, PCAP, host export, or a mix.
- [ ] Decide acquisition method; acquire a verified copy, never the original.

## 1. Preservation
- [ ] `sha256sum` every artifact; record the hash in the timeline.
- [ ] Record acquisition command, tool version, and time zone.
- [ ] Store the original read-only; work only on copies.

## 2. Memory (if a RAM dump exists)
> RAM dumps are analyzed with **Volatility 3** (external). DFTK has no RAM-dump
> parser — the `windows.*` names below are Volatility plugin arguments, not DFTK
> capabilities. Save Volatility output to the evidence root and cite it as a finding.
- [ ] `windows.info` → OS build / profile.
- [ ] `windows.pslist` / `windows.psscan` → processes.
- [ ] `windows.netscan` → connections (map to PCAP).
- [ ] `windows.cmdline` / `windows.malfind` → injected regions.

## 3. Host artifacts (Windows)
- [ ] Event logs: Security, PowerShell, Sysmon.
- [ ] Persistence: Run/RunOnce, services, scheduled tasks, WMI, startup.
- [ ] Execution: Amcache, Prefetch, Shimcache, BAM, UserAssist.
- [ ] Registry: USBSTOR, TERMSRV, last-logged-on.
- [ ] Browser: history/cookies/downloads (hand to DFTK browser parsers).

## 4. Timeline
- [ ] Build a Plaso super-timeline; export CSV/JSON.
- [ ] Fuse memory + host + any DFTK-parsed artifacts into one spine.

## 5. Network
- [ ] `tshark` conversation + DNS summary; export suspicious streams.
- [ ] Hand C2-like patterns to `malware-analysis/`; frame recovery to `protocol-reverse/`.

## 6. Handoff
- [ ] Every Finding cites an existing Evidence record with a reproducible command + hash.
- [ ] IOCs declassified by sensitivity tier.
- [ ] Case-review pass before final report.
