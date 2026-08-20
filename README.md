# DFTK Skill

The standalone Agent Skill for [DigiForensics/DFTK](https://github.com/DigiForensics/DFTK).

DFTK provides structured forensic capabilities and `Observation`/`Evidence` results. This repository contains the investigation guidance for defining evidence requirements, selecting capabilities, checking findings, and reporting their sources.

## Installation

The recommended installation path is to give an Agent the primary DFTK repository
URL:

```text
https://github.com/DigiForensics/DFTK
```

The Agent installs `dftk[mcp]`; `dftk agent setup --install-skill` then fetches this
matching DFTK-skill release into its own host directory and emits a reviewable MCP
configuration fragment. The exact, safe
sequence is in [INSTALL_AGENT.md](INSTALL_AGENT.md).

## Version

`3.4.0` — for DFTK `3.4.x`.

## Install

Install the complete skill directory, including `references/`, examples, templates, and `skills/`. The entry-point file alone is insufficient.

Common user-level locations:

```text
~/.agents/skills/dftk/
~/.kimi-code/skills/dftk/
~/.workbuddy/skills/dftk/
~/.claude/skills/dftk/
~/.codex/skills/dftk/
~/.hermes/skills/dftk/
```

Or install the matching release snapshot via `dftk skill --install` (fetches the `v{TOOLKIT_VERSION}` tag from this repo):

```bash
dftk skill --install
```

## Structure

```text
dftk/
  SKILL.md            # entry point and case-scoping guidance
  references/         # topic-specific guidance, loaded when needed
  examples/           # investigation examples
  templates/          # report templates
```

## Design boundary

This repository contains guidance and templates, not forensic parsers or an Agent runtime. Executable capabilities are provided by the `DFTK` repository and PyPI package.

The generated [capability catalog](references/capabilities.md) is tied to the
matching DFTK release manifest.

See [CONTRIBUTING.md](CONTRIBUTING.md) for documentation ownership and the specialist
skill format.

## Maintainer

- **Maintainer:** [DyNooob](https://github.com/DyNooob) — DigiForensics · [blog](https://buno.dev)
- **Organizations:** [DigiForensics](https://www.digiforensics.cn) · [LLMCN](https://www.llmcn.org)
- **License:** [Apache-2.0](LICENSE)
