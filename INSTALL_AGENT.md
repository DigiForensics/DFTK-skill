# Install DFTK from an Agent

DFTK, not this repository, is the primary Agent installation entry point. Give an
Agent this URL:

```text
https://github.com/DigiForensics/DFTK
```

After installing DFTK, `dftk agent setup --install-skill` fetches this complete
repository as an Agent Skill. It must not copy only `SKILL.md`: the bundle contains the common
investigation contract, specialist skills, and references used by those skills.

Once the Skill is available, the Agent installs its local runtime and the matching
DFTK-skill bundle for its own host:

```text
python -m pip install --upgrade "dftk[mcp]"
dftk agent setup --root <read-only-evidence-dir> --workspace <writable-case-dir> --install-skill
```

The bootstrap detects one current host when possible and otherwise falls back to
the portable `agents` directory. It creates a reviewable MCP configuration fragment
without overwriting host configuration. Do not install into every host by default.
The optional `--dry-run` prints destinations without changing them.

The MCP configuration is host-specific, but every host should launch:

```text
dftk mcp --root <read-only-evidence-dir> --workspace <writable-case-dir> --max-safety READ_ONLY
```

`--root` is read-only source scope. `--workspace` contains derived case material
and must be outside the root by default. See [MCP setup](references/mcp-setup.md)
for host configuration examples.
