---
name: protocol-reverse
description: Authorized reverse engineering of custom binary protocols, Protobuf/gRPC, WebSocket frames, and PCAP-driven protocol recovery. Use when the task is recovering a message layout, state machine, or serialization format from traffic or a client — not web parameter signing (use reverse-exe/mobile-reverse for that).
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - protocol
  - pcap
  - protobuf
  - reverse-engineering
---

# Protocol Reverse Engineering

Recover the structure of a custom or undocumented protocol from traffic captures, proxy exports, client logs, or binaries. The output is a message dictionary, a state machine, and a reproducible decoder — not an exploit.

## Operating contract

- Work within an authorized scope; replay only against systems you are authorized to test.
- Redact sensitive fields (credentials, tokens) in any shared output.
- Record SHA-256 of the PCAP and reproducible decode commands; enable the DFTK 3.3.0 audit ledger.

## When this skill applies

- Custom TCP/UDP binary protocols.
- Protobuf / gRPC / FlatBuffers / MessagePack.
- WebSocket / MQTT / private RPC.
- PCAP / PCAPNG field and state-machine recovery.
- Client–server checksums, sequence numbers, encrypted frame headers.

## Not this skill
- HTTP parameter signing / JS crypto → `reverse-exe` / `mobile-reverse` (or the `js-reverse` module).
- Firmware protocol stack + emulation → `firmware-pentest` first, then back here.

## Workflow

### Phase 1 — Capture & triage
```text
□ Obtain: PCAP / proxy export / client log / binary.
□ Mark direction: C→S / S→C; handshake, heartbeat, reconnect?
□ Fixed header? magic? length field? TLV? fixed-width?
□ Compression (zlib/gzip/lz4) or in-frame crypto (AES/ChaCha)?
□ tshark -r cap.pcap -T fields -e frame.number -e ip.src -e tcp.payload
```

### Phase 2 — Frame layout
```text
□ Align multiple same-type messages; find invariant bytes / incrementing sequence numbers.
□ Length field: big/little endian, includes header or not.
□ Checksum: CRC16/32, checksum, HMAC location.
□ Draw the state machine: Connect → Auth → Ready → Request/Response → Close.
□ Tools: Wireshark custom dissector draft, ImHex / 010 Editor template, Kaitai Struct.
```

### Phase 3 — Serialization & crypto
```text
□ Protobuf: recover .proto (blackboxprotobuf / pbtk / protoc --decode_raw).
□ gRPC: HTTP/2 headers + protobuf body.
□ Crypto: find key derivation in the client (so/dll/JS) → hand to reverse-exe / mobile-reverse.
□ Replay only within authorized scope; harmless fields first.
```

### Phase 4 — Artifacts (MUST produce)
```text
- Message-type table (name / opcode / fields).
- At least one reproducible decode command or script.
- Evidence: original hex excerpt + decoded result (redacted).
```

## Tooling
| Tool | Needed | Use |
|---|---|---|
| tshark / Wireshark | recommended | PCAP parsing |
| Python 3 | yes | decode scripts |
| blackboxprotobuf | optional | unknown protobuf |
| ImHex / 010 | optional | structure templates |
| IDA / r2 / Ghidra | as needed | client serialization functions |

## Domain references
- frame layout & Protobuf quick reference → `references/protocol-workflow.md`
- related: `../reverse-exe/`, `../mobile-reverse/`, `../malware-analysis/` (C2), `../digital-forensics/` (traffic forensics)

## Quality bar
A defensible protocol pass recovers a message layout or state machine (not just pasted hex), ships a reproducible decoder, respects scope, and redacts sensitive fields.

---

