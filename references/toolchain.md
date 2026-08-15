# External toolchain preparation (environment prep)

Use this when DFTK is installed alongside a shipped forensic-toolkit zip (IDA /
Ghidra / jadx / apktool / tshark / …) and the tools must be usable by `dftk`.

## The problem this solves

External binaries must be resolvable for `dftk_run` to stop returning
`unsupported`. If the toolkit is extracted somewhere the agent sandbox cannot
read, or onto a drive that is not on PATH, the tools are silently unusable.

`dftk prepare` fixes this without manual PATH edits and without admin rights.

## Steps for the recipient

1. Install DFTK and the skill (per `SKILL.md` §1 / the deployment notes).
2. Extract the forensic-toolkit zip to any writable directory, e.g. `E:\TOOLKIT`.
   The drive letter does not matter.
3. Run once:

   ```bash
   dftk prepare E:\TOOLKIT
   ```

4. Verify:

   ```bash
   dftk doctor
   ```

   The `external` section should show each tool `available: true` with `source`
   `DFTK_TOOLS / dftk prepare root` (or `dftk prepare shims`); the `toolchain`
   section shows `toolkit_root` and `bin_dir`.

After this, DFTK resolves the tools on every later call automatically — no PATH
change, no per-session setup needed for `dftk run` itself.

## What `dftk prepare` does

- Writes `~/.dftk/toolchain.json` recording `toolkit_root` and `bin_dir`. This
  file lives under the user home, so the agent can always read it even when the
  toolkit is on an exotic / non-PATH drive.
- Generates `bin_dir` launchers: `<tool>.bat` (Windows terminals) and an
  extensionless `<tool>` wrapper (agent Bash).
- Writes `set_path.bat` / `set_path.sh` so bare tool names also work in a plain
  terminal for that session only.

## Options

- `dftk prepare <root> --bin-dir <dir>` — put shims in a custom dir (e.g. a case
  workspace).
- `dftk prepare <root> --no-shims` — only record the root; no launchers.
- `dftk prepare <root> --rewrite-from <OLD_ROOT>` — rewrite a stale hardcoded
  absolute root inside the bundle's launcher scripts to the real toolkit root.
- `dftk prepare --show` — print the current toolchain config.

## Fallbacks (locked / lab machines)

- **PATH / registry writes blocked:** irrelevant — `dftk prepare` never needs
  them. Source `set_path.bat` / `set_path.sh` per session only if bare-name
  access is wanted.
- **Only a portable JDK (Ghidra/jadx need 21+):** bundle the JDK under the
  toolkit; DFTK discovery is unaffected.
- **PyPI unreachable:** DFTK core has zero mandatory dependencies; `pip install
  dftk` (no extras) still works.
- **Extracted onto exFAT / USB:** prefer `dftk prepare` (config-based, no `+x`
  bit needed); do not rely on `+x` on a non-NTFS volume.

## Gating

A tool depending on an external binary declares `requires=("jadx",)`. If absent,
`dftk_run` returns `unsupported` naming the missing binary. After `dftk prepare`,
the same tool resolves the binary from the recorded root and runs. No per-deployment
code change is required.
