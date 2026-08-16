# apk-reverse

Tool-driven Android APK reverse-engineering methodology: `jadx` Java
decompilation, `apktool` unpacking / smali & Manifest inspection, `frida`
dynamic observation, and native `.so` triage.

- Read-only-first; dynamic observation only on an authorized device / isolated
  emulator. Patching / repackaging only for apps you own or are authorized to
  assess.
- Complements the read-only `apk` module (static forensic triage) and hands off
  `.so` work to `ida-reverse` / `radare2`.
- Pairs with DFTK's audit ledger for process provenance.

## Files

- `SKILL.md` — the methodology.
- `references/frida-recipes.md` — starter Frida hook scripts.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
