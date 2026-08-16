---
name: firmware-forensics
description: >-
  Defensive firmware / IoT analysis — extract, dissect, and assess device firmware
  (routers, cameras, embedded appliances) following the OWASP FSTM stages. Read-only
  by default: information gathering, acquisition, static analysis, filesystem
  extraction, and emulation. Validation of a suspected flaw is done only in an
  isolated lab, and findings go through responsible disclosure — never weaponization.
  Pairs with reverse-exe / ida-reverse / radare2 for extracted binaries and with
  binary-diff for cross-version symbol migration.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - dfir
  - firmware
  - iot
  - embedded
---

# Firmware forensics (OWASP FSTM)

Methodology for the **defensive** analysis of device firmware: taking a `.bin` /
`.img` / OTA package and working through acquisition, static analysis, filesystem
extraction, and emulation to assess what the device actually runs. This supports
device assurance, incident response (compromised appliance), and responsible
vulnerability disclosure — not offensive exploitation.

This is a **methodology skill**. The tools are external; nothing here is bundled in
the `dftk` wheel. For extracted ELF/`.so`, hand off to `reverse-exe` / `ida-reverse`
/ `radare2`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working so
  the analysis process (hashes, extraction commands, emulation steps) is recorded.
- `dftk hash` is the DFIR-preferred hashing for the firmware image and each extracted
  artifact.
- Hand off a suspicious extracted binary to `malware-analysis`; hand off the device's
  network protocol to `protocol-reverse`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the firmware before anything else; analyze a copy.
2. **Isolated only.** Emulation, fuzzing, and any dynamic work happen in an isolated
   lab network — never against production devices you do not own.
3. **Authorized scope.** Analyze firmware for devices you own or are authorized to
   assess. Production OT/ICS devices require written authorization (see `ot-ics`).
4. **Validate, don't weaponize.** If a flaw is found, confirm impact in the isolated
   lab, then report via coordinated/responsible disclosure. Do not build or deploy
   exploit payloads.
5. **Record provenance.** Each finding cites: source, locator, value, hash.

## OWASP FSTM stages (defensive mapping)

```text
firmware .bin
  ├─ Stage 1-3: Information gathering / acquisition / analysis (header, entropy, strings)
  ├─ Stage 4: Filesystem extraction  ← binwalk v3 / unblob / jefferson / ubi_reader
  │     └─ failure → bootloader decrypt routine / UART dump / SPI flash read
  ├─ Stage 5: Filesystem static analysis  ← EMBA automated + manual grep
  ├─ Stage 6: Emulation  ← Firmadyne / FAT / qemu-user-static + chroot
  ├─ Stage 7-8: Dynamic / runtime analysis (isolated lab only)
  └─ Stage 9: Flaw validation + responsible disclosure (NOT exploitation)
```

Key judgments:
- Extraction failure ≠ encryption. Run binwalk v2/v3, unblob, jefferson, ubi_reader
  before assuming crypto.
- EMBA's one-command HTML report saves most of the legwork; verify each flagged CVE
  against the actual version string and exploit conditions.
- Emulation failing usually means missing NVRAM, wrong NIC name, or missing `/dev/`
  nodes.
- ARM/MIPS payloads differ by endianness (mipsel vs mipseb) — note it in the report.

## Stage 1 — Information gathering

Collect model, chip, SDK, and any published CVE.

```bash
# FCC ID lookup (US devices)
curl -s "https://fccid.io/?q=$FCC_ID"
# Chip families: Realtek RTL8197 / Broadcom BCM / MediaTek MT76 / Qualcomm IPQ
```

Output: chip model, SDK source (SDK dictates binwalk success), known CVE list.

## Stage 2 — Acquisition

Four routes: vendor download, OTA capture, UART shell dump, SPI flash physical read.

```bash
# OTA capture then bulk download
mitmdump -s save_response.py

# UART (USB-TTL, common baud 57600 / 115200)
picocom -b 115200 /dev/ttyUSB0

# SPI flash read with CH341A + flashrom
flashrom -p ch341a_spi -r dump.bin
```

Always SHA-256 every image you obtain.

## Stage 3 — Analyze (pre-extraction)

```bash
binwalk firmware.bin              # magic scan
binwalk -E firmware.bin           # entropy graph (high = compressed/encrypted)
strings -n 8 firmware.bin | less  # banner / kernel version / paths
file firmware.bin
hexdump -C firmware.bin | head -64
```

## Stage 4 — Extract filesystem

See `references/extraction.md`.

```bash
binwalk -eM firmware.bin           # recursive extract
unblob -d out/ firmware.bin        # formats binwalk misses
jefferson rootfs.jffs2 -d rootfs/  # JFFS2
ubireader_extract_files rootfs.ubi # UBI
```

## Stage 5 — Filesystem static analysis

EMBA automated scan, then manual confirm.

```bash
sudo emba -l ./logs -f ./firmware.bin -p ./scan-profiles/default-scan.emba
```

Manual:

```bash
grep -rE "(password|passwd|admin|secret|api_key|token)=" squashfs-root/
find squashfs-root/ -name "*.conf" -o -name "*.ini" -o -name "shadow"
checksec --file=squashfs-root/usr/sbin/httpd
```

## Stage 6 — Emulation (isolated lab)

```bash
# User-mode: single binary
qemu-mipsel-static -L squashfs-root/ squashfs-root/usr/sbin/httpd
# Full-system: FAT (Firmadyne wrapper)
sudo fat.py firmware.bin
```

## Stage 7–8 — Dynamic analysis (isolated lab only)

Attach a debugger, capture traffic, observe behavior — strictly in the lab.

```bash
qemu-mipsel-static -g 1234 ./vuln_binary
gdb-multiarch ./vuln_binary -ex "target remote :1234"
```

Treat any crash as a *finding to report*, not a launch point for a payload.

## Stage 9 — Flaw validation & disclosure (NOT exploitation)

When a suspected flaw is found:

1. Reproduce it in the isolated emulation / lab device.
2. Document impact precisely (affected function, trigger, blast radius).
3. Report via the vendor's security/SRC program or coordinated disclosure.
4. Do **not** generate or deploy exploit payloads; the goal is device assurance and
   remediation, not weaponization.

## Quality bar

A defensible firmware-forensics pass hashes every artifact, extracts and analyzes the
filesystem, preserves provenance, and — if a flaw is found — validates it in an
isolated lab and routes it to responsible disclosure rather than exploitation.

---

licensed. Re-cast from offensive pentest to defensive firmware forensics. The original
