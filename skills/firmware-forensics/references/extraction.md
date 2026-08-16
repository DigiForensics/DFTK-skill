# Firmware extraction details

Extraction is the step most likely to fail; work the tools in order before assuming
encryption.

## Tool order

```bash
binwalk firmware.bin              # magic scan; note offsets
binwalk -eM firmware.bin          # recursive extraction
unblob -d out/ firmware.bin       # catches formats binwalk misses
jefferson rootfs.jffs2 -d rootfs/  # JFFS2
ubireader_extract_files rootfs.ubi # UBI / UBIFS
```

## Entropy triage

```bash
binwalk -E firmware.bin
```

- Steady ~0.95 segments → normal compression (squashfs/xz).
- Uniform ~0.99 across the whole image with no magic → likely encrypted or pure
  compression; inspect the first 256 bytes for a vendor header.

## Encrypted firmware fallback

If extraction yields nothing and entropy is uniformly high:

1. Obtain the bootloader (UART `md.b` at boot, or SPI flash physical read) — it
   usually contains the decrypt routine.
2. Reverse the bootloader (IDA / Ghidra) for `image_decrypt` before `do_bootm`; the
   key is typically AES-128-CBC hardcoded in `.rodata`.
3. Decrypt offline and re-run Stage 4:

```bash
openssl enc -d -aes-128-cbc \
  -K $(cat key.hex) -iv $(cat iv.hex) \
  -in encrypted_fw.bin -out decrypted.bin
binwalk decrypted.bin
```

If the bootloader is also encrypted, consult the SoC's first-stage ROM documentation;
some SoCs with secure boot have published fault-injection research.

## Notes

- Record each extraction command + the resulting rootfs path in the audit ledger.
- Hash every extracted artifact (`dftk hash`) for provenance.
- Never flash modified firmware to a physical device without a full chip dump first
  (flashrom / ch341a / minipro) as a rollback.
