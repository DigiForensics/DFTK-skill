# Worked engagement — Android app data-exfil triage

A realistic transcript of the orchestrator loop. Tool names, argument shapes, the
case-id format, and every `dftk_search_capabilities` result below were confirmed
against a live `dftk mcp` stdio session (3.3.0). `<…>` are analyst-supplied values.

## Step 1 — open the case

```
dftk_case(action="new", name="mobile-suspect-app")
→ { "ok": true, "case": { "case_id": "case-20260816T035037Z-b4d81b", "name": "mobile-suspect-app", "runs": [] } }
```
Keep `case-20260816T035037Z-b4d81b` — every later call uses this generated id, **not**
the name `mobile-suspect-app`.

## Step 2 — discover the capability (Chinese alias proves routing)

```
dftk_search_capabilities(query="短信", limit=5)
→ [ "recipe.android.appdata_triage", "android.apk_endpoints", "android.apk_inventory",
    "android.apk_manifest", "android.apk_search" ]
```
No `android.sms_extract` / `android.contacts_extract` exist — those are not DFTK
capabilities. For a communications / data-exfil hypothesis the real capabilities are
`android.apk_endpoints` (network endpoints embedded in the APK) and
`recipe.android.appdata_triage` (inventory of extracted app data + permissions).

## Step 3 — read the contract

```
dftk_describe(name="android.apk_endpoints")
→ { "capability": { "name": "android.apk_endpoints", "safety": "READ_ONLY",
     "network": false,
     "parameters": { "properties": { "path": {"type":"string"}, "limit": {"type":"integer"} } } } }
```
Note: `name` is the **capability** `android.apk_endpoints`, never an MCP tool like
`dftk_doctor`.

## Step 4 — execute (persists seq=1)

```
dftk_run(name="android.apk_endpoints", params={"path":"/evidence/app.apk","limit":50},
         case_id="case-20260816T035037Z-b4d81b")
→ { "ok": true, "run": { "seq": 1, "tool": "android.apk_endpoints", "safety": "READ_ONLY" } }
```
⚠️ The `ok:true` above is the **request** acknowledgement, not a result. **Verify the
result** in Step 5: the top-level `ok` now reflects the run outcome
(`true` = `ok`/`partial`, `false` = `unsupported`/`error`/`blocked`). When `ok` is
`false`, read `observation.status` for the reason and `observation.errors[]` to fix
and re-run (new `seq`).

## Step 5 — page the result (no re-run)

```
dftk_read_case_run(case_id="case-20260816T035037Z-b4d81b", seq=1,
                   evidence_offset=0, evidence_limit=20)
→ { "ok": true, "observation": { "tool": "android.apk_endpoints",
    "status": "ok",
    "evidence": [ "https://api.example.com/collect", "http://203.0.113.7/beacon", … ] } }
```

> Branch on the top-level `ok` (`true` = real result, `false` = no usable result).
> When `ok` is `false`, read `observation.status`: `unsupported` = wrong input type,
> `error` = read `observation.errors[]`. Re-run (new `seq`) to fix.

## Step 6 — hand off

```
dftk_case(action="timeline", case_id="case-20260816T035037Z-b4d81b")
→ observation graph of every run
dftk_case(action="export", case_id="case-20260816T035037Z-b4d81b", format="md")
→ portable markdown report with full chain of custody
```

## Why this is defensible

- One case, every tool funnelled through it → continuous custody.
- `READ_ONLY` server ceiling meant no capability could mutate evidence or reach the
  network without an explicit, deliberate relaunch.
- Outputs are paged, not truncated blindly; the run is re-readable anytime via
  `dftk_read_case_run`.
- The export is self-contained and reviewable by a second analyst.
