---
name: ot-ics
description: >-
  Authorized OT/ICS security assessment — Purdue-model zoning, PLC/SCADA exposure,
  industrial-protocol discovery, and safe passive-first evaluation. Read-only by default;
  physical harm is possible from mistakes, so written authorization and a passive-first
  stance are mandatory. Use for reviewing an OT environment you own or are authorized to
  assess.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - ot
  - ics
  - scada
  - forensics
  - passive-first
---

# OT / ICS security

Methodology for the **defensive** assessment of Operational Technology / Industrial
Control Systems: mapping the Purdue zones, identifying assets and protocols, and finding
exposure — with a **passive-first** stance because mistakes here can cause physical harm.
The goal is asset visibility and safe hardening guidance, never disruption.

This is a **methodology skill**. The tools are external; nothing here is bundled in the
`dftk` wheel. For captured OT traffic, hand off to `protocol-reverse`; for controller
firmware, hand off to `firmware-forensics`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for any captured PCAP / config export.
- Pair with `threat-hunting` for detection engineering from observed traffic.

## Safety iron rules (MUST)

```text
MUST NOT, without explicit written permission:
- Write coils / registers to a PLC
- High-rate scan an entire production OT network
- Interrupt any Safety Instrumented System (SIS) path
Default: read-only identification, traffic mirroring, offline firmware/config analysis.
```

## Operating contract (passive-first, preserve, prove)

1. **Written authorization.** Scope must state site, network segment, and whether active
   scanning / register writes are permitted. Default = read-only.
2. **Passive-first.** Prefer SPAN/tap PCAP, config-file audit, and offline analysis over
   active interaction. Do not write to a control loop until `ready_for_act` is explicitly
   granted.
3. **Record provenance.** Each finding cites the asset, protocol, and observation, plus the
   authorized boundary it stayed within.
4. **Physical-impact note.** Every finding states its potential process/safety impact.
5. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED /
   UNSUPPORTED.

## Workflow

### Phase 1 — Zoning & assets

```text
□ Purdue L0–L5 sketch: field devices -> control -> supervisory -> site DMZ -> enterprise
□ Asset inventory: PLC / RTU / HMI / engineering station / historian / jump host
□ Protocol & port baseline (authorized segments only)
```

### Phase 2 — Passive & read-only

```text
□ SPAN/mirrored PCAP -> protocol-reverse / Wireshark OT dissectors
□ Offline audit of config & engineering files (TIA / RSLogix exports, etc.)
□ Default creds & cleartext protocols (Modbus has no auth) recorded as Findings, not altered
```

### Phase 3 — Limited active (authorized only)

```text
□ Low-rate identification, maintenance window only
□ Read-only function codes preferred
□ Evidence per step; stop and report on any anomaly
```

### Phase 4 — Firmware / patch surface

```text
□ Controller firmware version -> CVE mapping (do NOT blind-flash firmware)
□ Pair with firmware-forensics for offline image analysis
```

## Tool chain

| Tool | Use | Note |
|------|-----|------|
| Wireshark OT dissectors | Passive parse | Mirrored traffic |
| Nmap NSE (limited) | Identification | Rate + time window |
| Claroty / Nozomi class | Asset discovery | Commercial / on-site |
| Vendor engineering software | Config audit | Offline-first |
| binwalk / Ghidra | Firmware | Offline |

## Quality bar

A complete OT pass defaults to passive/read-only, records the authorized boundary, avoids
writing to control loops, states physical/process impact per finding, and leaves a
reproducible, safety-aware report.

---

