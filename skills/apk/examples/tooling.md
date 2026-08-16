# APK native tooling

Extracting and inspecting the native libraries (`.so`) that ship inside an APK.
Work on a copy; `dftk hash` the APK and each `.so` for fixity.

## Extraction

```bash
unzip -o app.apk -d app_unpacked
# Native libs live under lib/<abi>/  (armeabi-v7a, arm64-v8a, x86_64, …)
find app_unpacked/lib -name '*.so'
# Or decompile the whole package for context
apktool d app.apk -o app_dec
```

## Inspection

| Check | Command | What it tells you |
|-------|---------|------------------|
| Security mitigations | `checksec --file=lib/arm64-v8a/libfoo.so` | RELRO / PIE / NX / canary |
| Exported symbols | `readelf -sW libfoo.so` | Function names if not stripped |
| Imports | `objdump -d -j .plt libfoo.so` | Crypto / network libraries linked |
| Sections | `readelf -SW libfoo.so` | `.rodata` (strings/keys), `.text` size |

## Cross-links
- Key / string recovery from the `.so` → `string-and-key-recovery.md`.
- Android decompile / review playbook → `../SKILL.md`, `../../apk-reverse/`.
