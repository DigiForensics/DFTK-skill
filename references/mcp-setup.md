# DFTK MCP server setup

DFTK includes a local MCP server (`dftk.mcp_server`) named `DFTK`. It exposes the
toolkit to MCP-compatible clients over **stdio**. The server applies its own safety,
network, root, and timeout policy; clients cannot change that policy through tool
arguments.

Any host that can launch a stdio MCP server can use it. Configure a launch entry for
`dftk mcp --root <evidence_dir>`.

## 0. Recommended Agent bootstrap

Start from the primary DFTK repository, not from a copied Skill directory. After
installing `dftk[mcp]`, an Agent can prepare its own bounded integration in one
reviewable command:

```bash
dftk agent setup \
  --root /abs/path/to/evidence \
  --workspace /abs/path/to/case-workspace \
  --install-skill \
  --config-out /abs/path/to/case-workspace/dftk-agent-config.json
```

The command installs the DFTK-skill release matching the installed runtime and emits
two importable fragments: portable JSON (`mcp_json`) and Codex TOML (`codex_toml`).
It intentionally does **not** modify a host's global MCP configuration; import the
fragment using the host's normal UI/configuration workflow and approve the server.
Use `--dry-run` first when the Agent must show its intended destinations and policy.

## 1. Install

```bash
pip install "dftk[mcp]"   # installs a supported mcp release (>=2.0.0,<3)
dftk doctor                # verify the MCP dependency + which external tools exist
```

`dftk_doctor` also reports, in an `external` section, which external forensic
binaries (jadx, apktool, tshark, ghidra, radare2, …) are present on the host —
pure discovery, no execution.

## 2. Launch (stdio)

```bash
dftk mcp --root /abs/path/to/evidence \
         --workspace /abs/path/to/case-workspace \
         --max-safety READ_ONLY \
         --timeout 180 \
         --audit                 # optional: chain-of-custody ledger -> <workspace>/audit.jsonl
# add --allow-network to opt into capabilities that declare network access
```

Flags:

| Flag | Default | Meaning |
|------|---------|---------|
| `--root DIR` | `.` | Filesystem evidence root the server confines every path parameter to. Path escapes are rejected. |
| `--workspace DIR` | `$DFTK_WORKSPACE` or `~/.dftk` | Writable DFTK case workspace. It must be **outside `--root`** by default, so derived data never changes acquired evidence. |
| `--allow-workspace-in-root` | off | Explicit exception for legacy workflows that intentionally store derived data in the evidence root. |
| `--max-safety` | `READ_ONLY` | Capability safety ceiling: `READ_ONLY` or `STATEFUL`. |
| `--allow-network` | off | Opt-in for capabilities that declare network access. |
| `--timeout` | `180` | Hard timeout (seconds) for one capability run. |
| `--audit [PATH]` | off | Append every run to a JSONL chain-of-custody ledger (default `<workspace>/audit.jsonl`). |

## Verify the server

The server has no port or URL. An MCP host launches it as a child process and uses
JSON-RPC over stdin/stdout. Confirm that it starts and remains running before adding
it to your MCP configuration:

```bash
# 1) dependency + policy sanity (no server needed)
dftk mcp --root /abs/path/to/evidence --workspace /abs/path/to/case-workspace --check

# 2) boot in a terminal; it should print nothing and wait on stdin. Ctrl-C to stop.
dftk mcp --root /abs/path/to/evidence --workspace /abs/path/to/case-workspace --max-safety READ_ONLY
```

If `dftk mcp` prints a traceback or exits immediately, resolve the cause in the
troubleshooting table. Then configure the host and enable the server according to the
host's normal approval flow.

## 3. Tools exposed (server name: `DFTK`)

| Tool | Signature | Purpose |
|------|-----------|---------|
| `dftk_doctor` | `()` | Health + the server-owned MCP safety/root/network/timeout policy. |
| `dftk_search_capabilities` | `(query="", tags=None, produces=None, limit=12)` | Discover capabilities by evidence intent, tags, or produced-evidence type. Supports Chinese aliases (联系人, 短信, 通话, 流量, 注册表, 浏览器, 时间, 哈希, 邮件, …). |
| `dftk_describe` | `(name)` | Exact parameter / safety / dependency / tag / produced-evidence contract for one capability. |
| `dftk_run` | `(name, params=None, case_id=None)` | Execute one capability under server policy; optionally persist it in an existing case. |
| `dftk_case` | `(action, case_id=None, name=None, format="json", path=None, objective=None, max_steps=2)` | Manage the CaseSession: `new`, `list`, `show`, `guided_intake`, `brief`, `next`, `timeline`, `graph`, `export`. `guided_intake` persists intake plus selected child runs; `brief` is a bounded recovery/handoff checkpoint; `next` returns an action queue; `graph` correlates source-linked entities. |
| `dftk_read_case_run` | `(case_id, seq, evidence_offset=0, evidence_limit=20, fact_path="", value_offset=0, value_limit=50)` | Page one already-persisted Observation **without rerunning** the capability. |

## 4. Server policy

- **Evidence-root confinement** — every path-like parameter is validated to stay
  inside `--root`; escape attempts return an error, never a silent allow.
- **Safety ceiling** — a capability whose safety exceeds `--max-safety` is returned
  as `blocked`, not executed.
- **Network gating** — network-declaring capabilities are blocked unless
  `--allow-network` was set at launch.
- **Remote collection** — `server.remote_snapshot` accepts only fixed read-only
  SSH collection profiles; it has no arbitrary command parameter. Unknown SSH host
  keys are rejected and must be verified in the local `known_hosts` store first.
- **Output bounding** — results larger than 512 KB return a truncated preview and a
  `guidance` field; page the full persisted Observation with
  `dftk_read_case_run`.
- **Destructive always off** — `destructive_allowed` is `False` and not configurable.
- **Serialized runs** — a lock protects the case-manifest sequence during concurrent
  requests.

## 5. Connect an MCP host

Merge the server into your host's MCP config (WorkBuddy example: `~/.workbuddy/mcp.json`, add to the `mcpServers` object):

```json
{
  "mcpServers": {
    "dftk": {
      "command": "dftk",
      "args": ["mcp", "--root", "/abs/path/to/evidence", "--workspace", "/abs/path/to/case-workspace", "--max-safety", "READ_ONLY"]
    }
  }
}
```

Enable the `dftk` server in the host's connector settings. The six `dftk_*` tools
will then be available to the host.

> `dftk` must be installed (`pip install "dftk[mcp]"`) and on `PATH`. If your
> interpreter is a venv, point `command` at its `python` and use
> `args: ["-m", "dftk.cli", "mcp", "--root", "/abs/path/to/evidence", …]`.

## 6. MCP vs CLI

Use MCP when the host exposes the tools; the server enforces its policy. When MCP is
unavailable, use the CLI (`direct-cli.md`) and apply the same safety and root scope
yourself.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: dftk` after install | not on `PATH` / wrong interpreter | use the venv form `python -m dftk.cli mcp …`, or `pip install` into the active interpreter |
| Server exits instantly / traceback on boot | `mcp` extra missing or workspace policy failure | `pip install "dftk[mcp]"`; run `dftk mcp --root <evidence> --workspace <case-dir> --check` |
| Capability returns `blocked` | safety exceeds `--max-safety` | raise the ceiling to `STATEFUL` only if authorized, or pick a `READ_ONLY` capability |
| Network capability blocked | `--allow-network` not set | relaunch with `--allow-network` (authorized use only) |
| Param rejected / "outside evidence root" | path escapes `--root` | pass a path inside `--root`; escapes are denied, never silently allowed |
| `--workspace` error | workspace is inside `--root` | use a separate writable case directory; only use `--allow-workspace-in-root` for an intentional legacy exception |
| Result truncated at 512 KB | output bounding | re-read the persisted Observation via `dftk_read_case_run` |
| `dftk_*` tools don't appear | server is disabled or unapproved | enable/approve `dftk` in the host settings; restart the session if needed |

## 8. Typical agent flow (worked example)

1. **Health / policy** — `dftk_doctor()` confirms the server is up and shows the
   active safety / root / network / timeout policy you are bound by.
2. **Discover** — `dftk_search_capabilities(query="微信聊天记录")` (Chinese alias
   supported) returns candidate capabilities with their tags.
3. **Contract** — `dftk_describe(name="…")` shows exact params, safety, dependencies,
   and the produced-evidence type.
4. **Run** — `dftk_run(name="…", params={…}, case_id="case-001")` executes under
   server policy; large output is truncated with a `guidance` string.
5. **Page the full result** — `dftk_read_case_run(case_id="case-001", seq=1)` reads
   the persisted Observation *without* re-running the capability.
6. **Manage the case** — `dftk_case(action="timeline", case_id="case-001")` to
   review, `dftk_case(action="export", …)` to hand off.

The Skill's per-skill `skills/<name>/examples/*.md` (e.g. `malware-analysis`,
`digital-forensics`)
show the same steps written as concrete MCP calls.

### 8.1 Reading results correctly

Every `dftk_run` reply has the shape:

```json
{ "ok": true, "case_id": "…", "observation": { "tool": "…", "status": "ok|partial|unsupported|error|blocked", "summary": "…", "facts": {}, "evidence": [], "errors": [] } }
```

The top-level `ok` now **mirrors** the run outcome, so branch on it directly:

- `ok: true`  ⟺ `observation.status` is `ok` or `partial` — a usable result was produced; consume `evidence` / `facts`.
- `ok: false` ⟺ `observation.status` is `unsupported`, `error`, or `blocked` — no usable result; read `observation.status` for the reason and `observation.errors[]` for detail.

**Branch on `ok`, then read `observation.status` for the granular reason:**

| `observation.status` | When `ok` is | Meaning | Action |
| --- | --- | --- | --- |
| `ok` / `partial` | `true` | genuine result produced | consume `evidence` / `facts` |
| `unsupported` | `false` | input was not the expected type (e.g. a `.txt` handed to an APK capability) | pick the right capability or supply real evidence |
| `error` | `false` | the capability raised (missing param, bad type, missing dependency) | read `observation.errors[]`, fix the call |
| `blocked` | `false` | server policy refused (safety ceiling / network gate) | adjust launch policy or choose a permitted capability |

**Decision procedure:**

```
ok = reply.get("ok")
status = reply.get("observation", {}).get("status")
if ok:
    result = reply["observation"]          # safe to consume evidence / facts
elif status == "unsupported":
    # input was not the expected type for this capability
    # -> choose a different capability, or supply real evidence of the right kind
elif status == "error":
    # capability raised: missing param / bad type / missing dependency
    # -> read reply["observation"]["errors"] and correct the call, then re-run (new seq)
elif status == "blocked":
    # server policy refused (safety ceiling / network gate)
    # -> adjust launch policy or choose a permitted capability
```

Re-running to fix a failed call is safe: correcting params produces a **new** `seq`
inside the same case; the failed `seq` stays on the audit trail. Never declare a
finding from a run whose top-level `ok` is `false`.

## 9. Verified contract notes (from a live `dftk` 3.4.0 stdio handshake)

The following interface details were checked with an MCP client session:

- **`dftk_describe(name=…)` takes a DFTK *capability* name**, i.e. a value returned by
  `dftk_search_capabilities` such as `android.apk_endpoints` or `binary.pe_inventory`.
  It does **not** take an MCP tool name like `dftk_doctor` (that returns
  `unknown DFTK capability`).
- **`dftk_case` `show` / `timeline` / `export` need the *generated* `case_id`** returned
  by `dftk_case(action="new", …)` — e.g. `case-20260816T034157Z-ea679b`. The friendly
  `name` you passed at creation is **not** accepted by later actions
  (`no such case: <name>`).

### Verified transcript (abridged)

```text
$ dftk mcp --root /evidence --max-safety READ_ONLY   # stdio; no port/URL
initialize → protocolVersion "2025-11-25"
tools/list  → 6 tools: dftk_doctor, dftk_search_capabilities, dftk_describe,
              dftk_run, dftk_case, dftk_read_case_run

dftk_case(action="new", name="verified-demo")
  → { "ok": true, "case": { "case_id": "case-20260816T034157Z-ea679b", … } }

dftk_search_capabilities(query="短信", limit=3)
  → capabilities: recipe.android.appdata_triage, android.apk_endpoints, …

dftk_describe(name="android.apk_endpoints")
  → { "safety": "READ_ONLY", "network": false,
      "parameters": { "properties": { "path": {…}, "limit": {…} } } }

dftk_case(action="timeline", case_id="case-20260816T034157Z-ea679b")   # generated id, not name
dftk_case(action="export",   case_id="case-20260816T034157Z-ea679b", format="md")
```

The example server uses stdio with root `/path/to/evidence` and the `READ_ONLY`
ceiling. After installing `dftk[mcp]`, add the server to the MCP host configuration
and enable it through that host's normal settings.
