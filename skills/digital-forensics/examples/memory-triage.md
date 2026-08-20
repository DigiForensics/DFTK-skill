# Worked example — memory + disk triage of a Linux server

A concrete triage flow that pairs DFTK's case model with standard forensics tools
(Volatility 3 for memory, Plaso/`log2timeline` for disk). Commands use **DFTK MCP**
first; CLI fallback in parentheses. Evidence root is `/evidence`, case
`linux-box-2026`.

> Scope note: DFTK has **no RAM-dump parser** and **no Plaso super-timeline builder**.
> Memory analysis and the Plaso layer are *external* tools. DFTK is used for the
> artifacts it genuinely parses — E01 image metadata (`image.e01_*`), file hashes,
> strings, and filesystem/observation timelines (`timeline.*`, `recipe.timeline.*`).
> All capability names below were confirmed against the live DFTK 3.4.0 registry.

## 0 — open the case

```
MCP:  dftk_case(action="new", name="linux-box-2026")
CLI:  dftk case new --name linux-box-2026
```

## 1 — discover what DFTK can actually run

```
MCP:  dftk_search_capabilities(query="E01 disk image")
      → [ "image.e01_inventory", "image.e01_filesystem_inventory", ... ]
      dftk_describe(name="image.e01_inventory")
CLI:  dftk list --tag image
```

Confirm you have a memory dump (`dump.raw`) and a disk image (`disk.E01`) before
going deep. The search shows DFTK exposes E01 *metadata* parsing — not a full
filesystem mount or a Plaso timeline.

## 2 — memory: profile + processes + network (EXTERNAL — Volatility 3)

DFTK cannot parse a RAM dump. Run Volatility 3 directly and preserve its output as
evidence:

```
vol -f dump.raw windows.info        # OS build / profile
vol -f dump.raw windows.pslist      # processes
vol -f dump.raw windows.netscan     # network connections
vol -f dump.raw windows.cmdline     # command lines
vol -f dump.raw windows.malfind     # injected / unmapped regions
```

Save each result under `/evidence/volatility/` (e.g. `netscan.txt`). These are
external artifacts; reference them in the case notes, but do **not** call them via
`dftk_run` — there is no `memory.*` capability.

## 3 — disk image via DFTK (E01 metadata)

```
MCP:  dftk_run(name="image.e01_inventory",
               params={"path":"disk.E01"}, case_id="<id>")
      dftk_run(name="image.e01_filesystem_inventory",
               params={"path":"disk.E01","entry_limit":2000}, case_id="<id>")
CLI:  dftk run image.e01_inventory --params '{"path":"disk.E01"}' --audit .dftk/audit.jsonl
      dftk run image.e01_filesystem_inventory --params '{"path":"disk.E01","entry_limit":2000}' --audit .dftk/audit.jsonl
```

`image.e01_inventory` reads segment/media metadata (requires `pyewf`);
`image.e01_filesystem_inventory` inventories partitions and bounded root entries
(requires `pyewf` + `pytsk3`). If a dependency is missing, `dftk_run` reports the
gap — install it or note it; do not fall back to arbitrary shell mutation of
evidence.

> **Verify every DFTK run.** `dftk_run` returns an honest top-level `ok` (`true` for
> `ok`/`partial`, `false` for `unsupported`/`error`/`blocked`). After each call, branch on
> `ok`; when `false`, read `observation.status`: `unsupported` = wrong input type (pick the
> right capability); `error` = read `observation.errors[]` and re-run (new `seq`). Never
> declare a finding from a run whose top-level `ok` is `false`. (See
> `../../../references/mcp-setup.md` §8.1.)

## 4 — timeline (Plaso external + DFTK observation fusion)

Build the Plaso super-timeline externally, then use DFTK to fuse DFTK Observations
with the external findings:

```
# external: Plaso super-timeline from the extracted/mounted FS
log2timeline.py --storage-file /evidence/case.plaso /evidence/extracted_fs
psort.py -o json /evidence/case.plaso > /evidence/timeline.json

# DFTK: unified timeline from the extracted FS tree + Volatility socket list
MCP:  dftk_run(name="recipe.timeline.unified",
               params={"root":"/evidence/extracted_fs","limit":500}, case_id="<id>")
      dftk_run(name="timeline.merge",
               params={"files":["/evidence/case.plaso.dftk.json"],
                        "inline":[{"source":"volatility.netscan",
                                   "events":[{"time":"2026-01-04T03:14:22Z",
                                              "kind":"network",
                                              "detail":"listening socket 10.0.0.9:4444"}]}],
                        "limit":1000}, case_id="<id>")
CLI:  dftk run recipe.timeline.unified --params '{"root":"/evidence/extracted_fs","limit":500}' --audit .dftk/audit.jsonl
```

`recipe.timeline.unified` builds a source-attributed timeline from the filesystem
evidence tree; `timeline.merge` combines DFTK Observation JSON with inline events
(the Volatility `netscan` socket, above) so external and DFTK findings share one
spine. Verify each `dftk_run` per the note in §3 (branch on the top-level `ok`; when
`false`, read `observation.status` for the reason).

## 5 — correlate

Cross-reference the Volatility `netscan` sockets (in `/evidence/volatility/netscan.txt`)
against the disk timeline to anchor a suspicious connection to a file-write event at
a specific timestamp. The case keeps both the DFTK Observations and the external
artifacts together, so the correlation is defensible.

## 6 — export the case record

```
MCP:  dftk_case(action="timeline", case_id="<id>")
      dftk_case(action="export", case_id="<id>", format="md")
CLI:  dftk case timeline <id> && dftk case export <id> --format md
```

### Notes
- DFTK is read-only and evidence-preserving; it never modifies `dump.raw` or
  `disk.E01`. The audit ledger (`--audit`) records every run for chain of custody.
- Memory and Plaso layers are external by design. Record their output to the
  evidence root and cite it in findings; only call `dftk_run` for capabilities that
  exist in the registry (verify with `dftk_search_capabilities`).
