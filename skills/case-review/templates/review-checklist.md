# Case Review Checklist

Run before any report handoff. Mark each item pass/fail; a single hard failure blocks handoff.

## Scope
- [ ] Authorization, scope, and network_profile recorded in `scope.md`.
- [ ] Target activity is within the authorized scope.

## Evidence
- [ ] Every artifact has a SHA-256 (or recorded reason why not).
- [ ] Every Evidence record has a reproducible command.
- [ ] No dangling Evidence ids referenced by Findings/workitems/timeline.

## Findings
- [ ] Every Finding references ≥1 existing Evidence id.
- [ ] Path steps (if any) carry allowed path_type + Evidence reference.
- [ ] Confidence stated on validated Findings.

## Timeline & work items
- [ ] Timeline entries cite sources.
- [ ] Work items map to Evidence or are explicitly closed.

## Fixity
- [ ] `sha256sum` of each case-local artifact matches its recorded hash (or omission explained).

## Verdict
- [ ] Strict-mode pass: handoff ready.
- [ ] Otherwise: list gaps, return to analysis, or pause for human review.
