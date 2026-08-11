# dftk skill

Agent skill for **dftk** — an evidence-preserving digital forensics (DFIR) toolkit.

This repo is the **standalone, canonical** copy of the `dftk` agent skill
(`SKILL.md`). It teaches an agent how to drive dftk's 66 read-only/stateful
forensic tools through a safety-gated Observation/Evidence contract.

It is published independently of the Python package so the skill can be
distributed, reviewed, and updated on its own — without rebuilding or
re-publishing `dftk` on PyPI.

## What it is

- `SKILL.md` — the skill definition: CLI commands, the `run_tool` Python API,
  the safety model (default read-only, network opt-in, no destructive tools),
  and guidance for an agent's planner.

## Install into an agent

Copy this folder to your agent's skills directory:

```bash
# WorkBuddy / compatible
cp -r . ~/.workbuddy/skills/dftk
```

Or, if you already have dftk installed, let it register itself:

```bash
pip install dftk
dftk skill --install          # registers to ~/.workbuddy/skills/dftk
```

## The toolkit (separate, required)

This skill only *instructs* an agent. The actual tools live in the `dftk`
package and must be installed separately:

```bash
pip install dftk             # base toolkit, zero hard dependencies
pip install "dftk[all]"      # + optional expert parsers (E01/TSK, Registry/EVTX, DKIM/SPF, SSH)
# or run without installing:
uvx dftk ...
```

Source & issues: https://github.com/DigiForensics/DFTK

## License

Apache License 2.0. Copyright 2026 DyNooob @ DigiForensics.
See [LICENSE](LICENSE).
