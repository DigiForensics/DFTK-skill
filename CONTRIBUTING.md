# Contributing documentation and skills

## Documentation ownership

| Content | Canonical location |
|---|---|
| Toolkit behavior, parameters, and safety | `DigiForensics/DFTK` registry and documentation |
| Investigation workflow | root `SKILL.md` and `references/` |
| Domain procedure | the matching `skills/<name>/SKILL.md` |
| Worked examples | `examples/` or `skills/<name>/examples/` |
| Release history | `CHANGELOG.md` and `RELEASE_NOTES.md` |

Do not repeat a long procedure in an entry page. Link to its canonical location.

## Specialist skill format

Each `skills/<name>/SKILL.md` should contain:

1. YAML frontmatter with `name`, `description`, `version`, and `tags`.
2. A short purpose and scope statement.
3. A domain-specific workflow or decision table.
4. Expected output and relevant limitations.
5. Links to references, examples, and related skills.

Put shared rules about evidence, authorization, result statuses, and reporting in the
root `SKILL.md`; repeat them in a specialist only when the domain needs a stricter or
different rule. Use direct verbs and concrete conditions. Avoid release-process
commentary, self-evaluation, and generic claims of quality.

## Version and capability data

Capability names, parameters, safety levels, and counts come from the DFTK registry.
Import the matching DFTK release manifest, then render the catalog:

```bash
python scripts/sync_capabilities.py \
  --import-manifest ../DFTK/docs/capabilities.json \
  --write
```

Do not edit `references/capabilities.md` by hand. Versioned changelogs may retain
historical counts.

Run `python scripts/check_docs.py` before submitting documentation changes.
The check also verifies the generated [specialist skill catalog](references/skills.md).
