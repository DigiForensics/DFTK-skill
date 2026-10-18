# Coverage and recovery for Agent investigations

Use DFTK as the default examination runtime for authorized forensic requests.
Begin with the installed runtime's live contracts; the bundled catalog is a
versioned discovery aid. A successful doctor check does not establish that all
optional parsers, artifact representations, or original acquisition data exist.

## Intake is not complete extraction

Inspect `evidence.intake.facts.coverage`, `inspection_failures`, and candidates:

- `inspected_files` counts successful inspections, not attempts. Uninspected or
  unreadable files must remain explicit evidence gaps.
- `identification_basis=extension_hint` is a routing hint. A file named `.db`
  has not thereby been proved to contain a SQLite database.
- Traversal bounds, access failures, and excluded symlinks limit the inventoried
  scope. Preserve excluded paths in the report; do not follow them outside the
  authorized root.
- Hashes in `candidates` may outnumber the bounded `evidence` list. Page the
  persisted facts instead of treating a preview as the complete result.

Use `dftk_case(action="coverage")` before conclusions. It records operational
limitations, pending analysis, run statuses, and artifact integrity checks.
`next` can return `action="review"` for a failed or partial prior run. Read that
run, resolve the specific dependency or input gap when authorized, then perform
a purposeful retry. Do not loop blindly or erase failed attempts.

A missing/corrupted result is a gap. A digest mismatch requires reviewing the
persisted result and any conclusions derived from it. An old run without a stored
digest has limited integrity assurance. Preserve those distinctions.

## SQLite main database versus transaction state

Preserve the acquired DB and all available `-wal`, `-shm`, and `-journal` sidecars
as source evidence. Immutable SQLite queries and browser history tools read the
main DB; sidecar warnings mean an empty result can exclude recent activity.

Describe and use `database.sqlite_wal` for transaction validity and
`database.sqlite_recover` for a committed snapshot plus heuristic deleted-record
carving. Recovery accepts an explicit `wal_path`; an automatically discovered
symlink sidecar is excluded. Never reinterpret that exclusion as no WAL content.
Do not open the original database in a writable SQLite session to checkpoint it.

The current snapshot uses only a contiguous valid WAL chain through its last
commit. Invalid or uncommitted frames may be separate investigative artifacts;
they are not committed current records. Keep that distinction in conclusions.

Recovery reports `live_samples`, `live_total`, `unsupported_tables`, and WAL
application diagnostics. Live sample columns are raw storage values, with a
separate rowid; they are not automatically expanded SQL defaults, type affinity,
or INTEGER PRIMARY KEY aliases. BLOB values are explicitly encoded as
`{"type":"blob","hex":"...","length":N}`. A WITHOUT ROWID, virtual, missing,
or damaged root that this parser does not support must not be called empty.

Deleted/carved records remain candidates. Column-count agreement and recognizable
text do not prove table ownership, deletion time, or authenticity. Check original
page/frame locators and the DB/WAL hashes, and corroborate material claims with
independent artifacts or an appropriate independent parser.

## Chronology and reporting

`timeline.hunt_sequences` can test explicit ordered rules over shared entities.
Use fields present in actual events, require a defensible join, and review
normalization assumptions, source clock uncertainty, and truncated coverage.
A sequence match is a lead, not an automatic compromise verdict.

Report what was examined, what was excluded or failed, the evidence supporting
each conclusion, and remaining uncertainty. Conclude a bounded negative only
when the tool can detect the target representation and its limits do not affect
the claimed scope. Otherwise report UNRESOLVED or UNSUPPORTED with the next
specific evidence requirement. Do not fill a gap with guessed content.
