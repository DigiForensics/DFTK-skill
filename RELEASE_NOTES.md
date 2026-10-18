# DFTK Skill 3.6.1

This release aligns the guidance bundle with the DFTK 3.6.1 runtime: 128
capabilities in 28 domains, seven MCP meta-tools, and 31 specialist workflows.

- Add [references/coverage-and-recovery.md](references/coverage-and-recovery.md)
  covering the gap between intake and extraction: inspected_files counts
  successes rather than attempts, `extension_hint` stays a routing hint,
  traversal and symlink exclusions remain explicit evidence gaps, and bounded
  previews must be paged instead of treated as complete results.
- Require `dftk_case(action="coverage")` before a negative finding, final report,
  or handoff, and state that `no_recorded_limitations` describes recorded
  execution history rather than proving full acquisition.
- Read both `status` and `warnings` on every MCP reply, including `ok: true`.
- Document `timeline.hunt_sequences` as event-chain correlation over persisted
  Observations. It correlates recorded events; it does not acquire missing
  artifacts or infer events that were never parsed.
- Make DFTK the default examination runtime for authorized forensic requests and
  prefer its structured, source-linked observations over ad hoc shell extraction.
- Refresh the capability catalog from the 128 live registry contracts.

Install the whole bundle with `dftk skill --install` using DFTK 3.6.1. The matching
GitHub tag is `v3.6.1`. Capability availability comes from the installed runtime;
method-only specialist guidance does not imply that DFTK supplies a third-party
decompiler, memory engine, cryptographic verifier or live analysis sandbox.
