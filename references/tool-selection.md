# Tool selection and replanning

## Search from the gap
Search DFTK capabilities for the evidence type needed, not for the answer you hope to find.

Good search intents:
- Android endpoint configuration / executable URL use
- authentication event remote IP
- SQLite schema and account relationship
- PCAP HTTP/DNS/TLS evidence
- filesystem timestamp inventory

Weak search intents:
- “answer question 7”
- the expected answer string copied from a guess

## Suggest from the input or required output

When `dftk_suggest` is available, pass a known evidence path, filename (`$MFT`,
`Amcache.hve`), or input kind (`pcap`, `registry`). It returns explained candidates
from the live registry. Relative MCP paths resolve under the server's evidence root.
Missing files can be planned from their names; header probes read at most 4096 bytes
from regular files. A signature/extension conflict is a reason to verify the type
with `artifact.inspect` before deeper analysis.

Use `direction="produce"` with a required output kind such as `tls_sni`,
`timeline`, or `partition_table`. This matches declared output kinds; it does not
predict what can be derived from an arbitrary input file and performs no file reads.

Check `why`, `reasons`, `requires`, `parameters`, and `policy_allowed` /
`policy_blockers`. Policy eligibility covers the safety/network gate only; it does
not prove the format is supported or dependencies are installed. Suggestions are
heuristics, not observations. Do not treat no matches as a negative forensic finding.
If an older server lacks `dftk_suggest`, use `dftk_search_capabilities` instead.

CLI equivalents:

```bash
dftk suggest capture.pcap
dftk suggest tls_sni --direction produce
```

## Describe before run
Check:
- exact parameter names/types;
- declared safety level;
- whether network is required;
- `produces` and tags;
- optional parser requirements;
- cost hint.

## Selection preference
When several capabilities could help:
1. prefer artifact-native structured parsers;
2. prefer direct evidence over broad discovery;
3. prefer low-cost bounded operations;
4. use string/byte search to discover candidates or when structured parsing cannot reach the target;
5. use a different evidence source for corroboration rather than repeating equivalent searches.

## Replanning
After an Observation, update the evidence gap. Replan when:
- the artifact type differs from expectation;
- a parser is unsupported;
- a candidate reveals a stronger structured source;
- warnings show incomplete coverage;
- the result disproves the current hypothesis.

Do not repeat an equivalent action with only cosmetic query changes unless the changed query tests a distinct hypothesis.
