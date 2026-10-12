# DFTK 3.5.0 Capability Catalog

Generated from the live DFTK 3.5.0 registry: **117 capabilities** across 24 domains.

This is a documentation snapshot. Prefer live `dftk_suggest`, `dftk_search_capabilities`, and `dftk_describe` when available. Suggestions are candidates; only actual Observations establish findings.

All tools preserve source evidence. `STATEFUL` tools write derived workspace output. Network access is separately gated.

## Domains

- `android` — 7 capabilities
- `application` — 2 capabilities
- `archive` — 2 capabilities
- `artifact` — 1 capabilities
- `binary` — 10 capabilities
- `browser` — 8 capabilities
- `case` — 2 capabilities
- `crypto` — 3 capabilities
- `database` — 10 capabilities
- `docker` — 2 capabilities
- `email` — 4 capabilities
- `encoding` — 1 capabilities
- `file` — 4 capabilities
- `filesystem` — 6 capabilities
- `image` — 3 capabilities
- `linux` — 4 capabilities
- `memory` — 6 capabilities
- `network` — 8 capabilities
- `recipe` — 14 capabilities
- `server` — 1 capabilities
- `timeline` — 2 capabilities
- `tree` — 1 capabilities
- `web` — 3 capabilities
- `windows` — 13 capabilities

## android

### `android.apk_endpoints`

Extract URL/domain/IP/content-URI endpoint candidates from parsed DEX strings across an APK with source DEX/string locators.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `endpoints`, `domains`, `urls`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 2000 |  |

### `android.apk_inventory`

Inventory APK ZIP members, DEX files, native libraries, certificates and manifest presence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `android.apk_manifest`

Parse AndroidManifest.xml from an APK, including binary AXML, and summarize package, permissions, SDK and components.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `android_manifest`, `permissions`, `components`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `include_elements` | boolean | no | False |  |

### `android.apk_search`

Search parsed DEX string tables inside an APK for a literal or regular expression.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `query` | string | yes |  |  |
| `regex` | boolean | no | False |  |
| `limit` | integer | no | 500 |  |

### `android.apk_signing_inventory`

Detect APK v1 signing entries and APK Signing Block scheme IDs (v2/v3/v3.1/source stamp) without modifying the APK.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `apk_signing`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `android.appdata_inventory`

Inventory an extracted Android app data directory (shared_prefs, databases, files, cache) without modifying it.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `android_appdata`, `database_candidates`, `shared_preferences`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `max_files` | integer | no | 20000 |  |

### `android.dex_strings`

Parse the DEX string table using ULEB128 string_data_item and modified UTF-8.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `contains` | string | no |  |  |
| `regex` | string | no |  |  |
| `limit` | integer | no | 10000 |  |

## application

### `application.profile_apply`

Detect (or explicitly select) an application artifact profile for a SQLite database and normalise its rows into canonical fields. Opens the database read-only. When no profile matches, the tool reports that explicitly instead of guessing.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `profile_records`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `profile_id` | string | no |  |  |
| `limit` | integer | no | 1000 |  |

### `application.profile_list`

List registered application artifact profiles (detection conditions, database locations, table/field mapping, time format, encoding, attachment relations).

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `profile_list`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|

## archive

### `archive.extract_safe`

Extract ZIP/TAR members into a separate workspace with path-traversal, symlink/junction, member-count and total-size limits. Source archive is never modified. Each extracted member is registered as a DerivedArtifact so the recovery chain is provable.

Safety: `STATEFUL` · Network: `false` · Cost: `medium`

Produces: `extracted_files`, `derived_artifacts`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `output_dir` | string | yes |  | WORKSPACE_OUTPUT |
| `member_limit` | integer | no | 20000 |  |
| `total_size_limit` | integer | no | 2147483648 |  |
| `overwrite` | boolean | no | False |  |

### `archive.inventory`

Inventory ZIP/TAR archive members and metadata without extraction. The member list is bounded by `limit` (peak memory stays proportional to `limit` even for very large archives).

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 10000 |  |

## artifact

### `artifact.inspect`

Identify an artifact from magic bytes and container structure, with size and SHA-256.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `artifact_type`, `hash`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

## binary

### `binary.elf_dynamic`

Parse ELF dynamic metadata: NEEDED libraries, interpreter, RPATH/RUNPATH, GNU build-id, and dynamic symbol table. Read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `elf_dynamic`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.elf_inventory`

Parse ELF architecture and section metadata; optionally extract bounded printable strings.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `strings` | boolean | no | True |  |
| `string_limit` | integer | no | 2000 |  |

### `binary.native_indicator_scan`

Heuristically scan a native binary for JNI names, crypto APIs, URLs and suspicious command/network indicators. Findings are indicators, not conclusions.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `native_indicators`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 1000 |  |

### `binary.pe_exports`

Parse the PE export table: exported symbols with ordinals and addresses, plus forwarded exports. Read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_exports`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.pe_headers`

Dump PE/COFF header structure: DOS/COFF/optional header fields, data directories and section summary. Read-only structural view.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_headers`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.pe_imports`

Parse the PE import table: DLLs and imported symbols (by name or ordinal). Computes Mandiant-compatible imphash. Read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_imports`, `imphash`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.pe_inventory`

Parse PE/COFF architecture, timestamp, characteristics and section table without executing the binary.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_metadata`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `strings` | boolean | no | False |  |
| `string_limit` | integer | no | 2000 |  |

### `binary.pe_resources`

Walk the PE resource tree (type/name/language) and extract the embedded application manifest (RT_MANIFEST). Read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_resources`, `manifest`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.pe_rich_header`

Decode the PE Rich Header: compiler/toolchain product IDs, versions and counts (linker, MASM, ImportLib). Read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_rich_header`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `binary.pe_signing`

Inspect Authenticode signature (WIN_CERTIFICATE / PKCS#7). Extracts embedded certificate chain issuer/subject/validity without external crypto libraries. Absence of a signature is reported, not assumed malicious.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `pe_signing`, `certificates`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

## browser

### `browser.chromium_bookmarks`

Read bounded Chromium Bookmarks JSON trees with folder paths, JSON-pointer locators and Windows-epoch microsecond timestamps; no browser launch or URL access.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_bookmarks`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `limit` | integer | no | 5000 |  |
| `max_bytes` | integer | no | 33554432 |  |
| `max_depth` | integer | no | 64 |  |

### `browser.chromium_cookies`

Inventory Chromium/Chrome/Edge Cookies SQLite metadata in immutable read-only mode. Plaintext values are omitted unless include_values=true; encrypted blobs are never decrypted.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_cookies`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `include_values` | boolean | no | False |  |
| `limit` | integer | no | 5000 |  |

### `browser.chromium_downloads`

Read Chromium/Chrome/Edge download records and URL chains from History SQLite in immutable read-only mode.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_downloads`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 5000 |  |

### `browser.chromium_history`

Read Chromium/Chrome/Edge History SQLite visits and URLs in immutable read-only mode.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_history`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 5000 |  |

### `browser.chromium_search_terms`

Read recorded Chromium keyword_search_terms with URL context. URL last_visit_time is context, not an exact search timestamp; never inferred as a search event.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_search_terms`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `limit` | integer | no | 5000 |  |

### `browser.firefox_bookmarks`

Read Firefox moz_bookmarks joined to moz_places in immutable mode, preserving folder relationships, GUIDs and creation/modification timestamps.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_bookmarks`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `limit` | integer | no | 5000 |  |

### `browser.firefox_cookies`

Read Firefox moz_cookies metadata in immutable read-only mode; redact plaintext values by default and normalize Unix second/microsecond timestamps.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_cookies`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `limit` | integer | no | 5000 |  |
| `include_values` | boolean | no | False |  |

### `browser.firefox_history`

Read Firefox places.sqlite history visits in immutable read-only mode.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_history`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 5000 |  |

## case

### `case.report_html`

Render a self-contained HTML forensic report from a list of Observations: case summary, evidence sources, observations, recovered artifacts, timeline, entities, warnings/limitations, chain of custody and tool manifest. STATEFUL: writes only to the workspace; the report is registered as a DerivedArtifact.

Safety: `STATEFUL` · Network: `false` · Cost: `medium`

Produces: `html_report`, `derived_artifact`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `output_dir` | string | yes |  | WORKSPACE_OUTPUT |
| `observations` | array | yes |  |  |
| `case_id` | string | no |  |  |
| `title` | string | no | DFTK Forensic Report |  |
| `audit_log` | string | no |  | WORKSPACE_INPUT |
| `name` | string | no | dftk_report.html |  |
| `timeline_limit` | integer | no | 2000 |  |

### `case.verify`

Verify an audit ledger's integrity and cross-check it against observations / a manifest. Validates the previous_hash → record_hash chain and re-derives each record's result and evidence digests. Reports VALID or BROKEN with the failing record number and reason.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `verification_report`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `audit_log` | string | yes |  | WORKSPACE_INPUT |
| `observations` | array | no |  |  |
| `manifest` | object | no |  |  |

## crypto

### `crypto.bip39_scan`

Scan one file or directory for BIP39 English word sequences and distinguish checksum-valid mnemonics.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `max_files` | integer | no | 5000 |  |
| `max_bytes_per_file` | integer | no | 8388608 |  |
| `max_candidates` | integer | no | 200 |  |

### `crypto.bip39_validate`

Validate a BIP39 English mnemonic including its checksum.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `mnemonic` | string | yes |  |  |

### `crypto.entropy_profile`

Compute bounded Shannon entropy per file block to highlight compressed/encrypted/high-entropy regions; does not classify encryption by itself.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `entropy_profile`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `block_size` | integer | no | 4096 |  |
| `block_limit` | integer | no | 100000 |  |

## database

### `database.sql_dump_inventory`

Inventory generic SQL text dumps (MySQL/PostgreSQL/SQLite-style) for databases, CREATE TABLE statements and INSERT counts without importing the dump.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `sql_schema`, `table_activity`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `max_bytes` | integer | no | 268435456 |  |
| `statement_limit` | integer | no | 200000 |  |

### `database.sqlite_deleted_records`

Carve deleted/candidate records from SQLite unallocated page space, freeblocks and freelist pages. Classifies each as DELETED_CANDIDATE (column count matches the live schema) or CARVED (record-shaped but unmatched).

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `deleted_records`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `max_bytes` | integer | no | 268435456 |  |
| `limit_per_table` | integer | no | 200 |  |

### `database.sqlite_forensic_inventory`

Forensic inventory of a SQLite database: 100-byte header fields (page size, change counter, freelist, schema cookie, autovacuum, encoding, page count) plus a page-type distribution. Uses a direct byte parser, not the SQLite engine.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `sqlite_header`, `page_distribution`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `max_bytes` | integer | no | 268435456 |  |

### `database.sqlite_freelist`

Enumerate the SQLite freelist: the trunk chain and every freelist leaf page, comparing against the header total. Freelist pages hold dropped table/record data.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `freelist`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `max_bytes` | integer | no | 268435456 |  |

### `database.sqlite_inventory`

Open SQLite in read-only URI mode and report objects, schemas and optional row counts.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `count_rows` | boolean | no | True |  |
| `table_limit` | integer | no | 500 |  |

### `database.sqlite_pages`

Enumerate every page in a SQLite database with its type, cell count, freeblock and fragmented-byte metadata. Low-level structural map.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `page_map`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `max_bytes` | integer | no | 268435456 |  |
| `page_limit` | integer | no | 100000 |  |

### `database.sqlite_query`

Execute one bounded read-only SELECT/WITH query against SQLite with SQLite authorizer write operations denied.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `query_rows`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `sql` | string | yes |  |  |
| `params` | array | no | [] |  |
| `limit` | integer | no | 1000 |  |

### `database.sqlite_recover`

Reconstruct the logical current database by overlaying valid WAL frames onto DB pages, then recover live + deleted records across all tables. The deepest SQLite recovery path.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `recovered_records`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `wal_path` | string | no |  |  |
| `max_bytes` | integer | no | 268435456 |  |
| `limit_per_table` | integer | no | 200 |  |

### `database.sqlite_search`

Search bounded SQLite tables/columns for a literal value using immutable read-only access; avoids requiring the Agent to construct schema-specific SQL first.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `database_matches`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `query` | string | yes |  |  |
| `case_sensitive` | boolean | no | False |  |
| `table_limit` | integer | no | 200 |  |
| `column_limit` | integer | no | 2000 |  |
| `result_limit` | integer | no | 1000 |  |

### `database.sqlite_wal`

Parse a SQLite WAL (-wal) file: header (magic, salts, checksums), and every frame with page number, commit flag, salt match and native-order checksum validity.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `wal_frames`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `wal_path` | string | yes |  |  |
| `db_path` | string | no |  |  |

## docker

### `docker.offline_inventory`

Recover Docker container configuration from an offline /var/lib/docker tree without starting Docker.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `limit` | integer | no | 1000 |  |

### `docker.offline_logs`

Read bounded Docker json-file container logs from an offline Docker data root, optionally filtering for a literal query.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `container_logs`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `query` | string | no |  |  |
| `limit` | integer | no | 5000 |  |

## email

### `email.auth_analyze`

Offline EML analysis of sender headers, DKIM identifiers and Authentication-Results. Header mismatches are context, not automatic spoofing verdicts.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `email.dkim_verify`

Verify DKIM signatures using dkimpy and DNS. This is signature verification, not DKIM-Signature repair.

Safety: `READ_ONLY` · Network: `true` · Cost: `low`

Produces: `dkim_verification`

Requires: `dkimpy`, `dnspython`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `email.mime_inventory`

Parse an RFC-style email file and inventory headers, MIME parts and attachment hashes without extracting or executing content.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `email_headers`, `mime_parts`, `attachments`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `include_body_preview` | boolean | no | False |  |
| `preview_chars` | integer | no | 1000 |  |

### `email.spf_verify`

Evaluate SPF for a supplied sending IP and SMTP envelope identity using pyspf and DNS; it does not infer IP from From headers.

Safety: `READ_ONLY` · Network: `true` · Cost: `low`

Produces: `spf_result`

Requires: `pyspf`, `dnspython`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `ip` | string | yes |  |  |
| `mail_from` | string | yes |  |  |
| `helo` | string | yes |  |  |

## encoding

### `encoding.decode_candidates`

Try common reversible text encodings (hex, Base64/Base64URL, percent-encoding) and return bounded decoded candidates with printable ratios.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `decoded_candidates`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `value` | string | yes |  |  |
| `max_output_bytes` | integer | no | 1048576 |  |

## file

### `file.hash`

Compute cryptographic hashes of one file without modifying it.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `algorithms` | array | no | ['sha256'] |  |

### `file.search_tree`

Search a file or directory tree for text/byte patterns with bounded results and source locators.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `search_matches`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `query` | string | yes |  |  |
| `regex` | boolean | no | False |  |
| `case_sensitive` | boolean | no | False |  |
| `max_files` | integer | no | 20000 |  |
| `max_file_size` | integer | no | 16777216 |  |
| `limit` | integer | no | 1000 |  |

### `file.strings`

Extract bounded printable ASCII strings with byte offsets.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `min_length` | integer | no | 4 |  |
| `limit` | integer | no | 5000 |  |

### `file.strings_unicode`

Extract bounded UTF-16LE/UTF-16BE printable strings with byte offsets; useful for Windows/native artifacts that ASCII strings miss.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `strings`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `min_length` | integer | no | 4 |  |
| `limit` | integer | no | 5000 |  |

## filesystem

### `filesystem.deleted`

List deleted file entries recovered from a filesystem. FAT volumes are recovered by the pure-Python reader; NTFS/ext unallocated recovery still requires pytsk3.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `deleted_entries`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `entry_limit` | integer | no | 2000 |  |

### `filesystem.extract`

Extract a byte range (raw offset or, with pytsk3, a file path) from a disk image into the workspace. The extracted file is registered as a DerivedArtifact (provenance). STATEFUL: writes only to workspace.

Safety: `STATEFUL` · Network: `false` · Cost: `medium`

Produces: `extracted_file`, `derived_artifact`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `output_dir` | string | yes |  | WORKSPACE_OUTPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `path_in_fs` | string | no |  |  |
| `offset` | integer | no | 0 |  |
| `length` | integer | no | 0 |  |
| `name` | string | no |  |  |
| `max_bytes` | integer | no | 1073741824 |  |

### `filesystem.list`

List the root (or given) directory of a filesystem inside a disk image. FAT volumes use the pure-Python reader (no external dependency); NTFS/ext/HFS+ still require pytsk3.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `directory_entries`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `path_in_fs` | string | no | / |  |
| `entry_limit` | integer | no | 2000 |  |

### `filesystem.read`

Read a byte range from a filesystem. With a filesystem backend (pytsk3 for NTFS/ext/HFS+, or the pure-Python FAT reader) + path_in_fs, reads that file; otherwise reads partition_offset+offset raw bytes. Returns a bounded hex preview + SHA-256.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `bytes_preview`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `path_in_fs` | string | no |  |  |
| `offset` | integer | no | 0 |  |
| `length` | integer | yes | 4096 |  |
| `preview_bytes` | integer | no | 1024 |  |

### `filesystem.stat`

Return filesystem metadata (size, timestamps, type, attributes) for a file/dir inside a disk image. FAT uses the pure-Python reader; NTFS/ext/HFS+ need pytsk3.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `file_stat`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `path_in_fs` | string | yes | / |  |

### `filesystem.walk`

Recursively walk a filesystem inside a disk image with depth/entry limits and optional deleted-entry inclusion. FAT uses the pure-Python reader; NTFS/ext/HFS+ need pytsk3.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `walk_entries`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `partition` | integer | no | 1 |  |
| `partition_offset` | integer | no | 0 |  |
| `path_in_fs` | string | no | / |  |
| `max_depth` | integer | no | 8 |  |
| `max_entries` | integer | no | 5000 |  |
| `include_deleted` | boolean | no | False |  |

## image

### `image.e01_filesystem_inventory`

Read E01/EWF through pyewf + pytsk3 and inventory volume partitions and bounded filesystem root entries without mounting or modifying evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `partition_table`, `filesystem_inventory`

Requires: `pyewf`, `pytsk3`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `entry_limit` | integer | no | 2000 |  |

### `image.e01_inventory`

Open an E01/EWF image read-only with pyewf and report segment/media metadata. Filesystem traversal is intentionally a separate future primitive.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `ewf_metadata`

Requires: `pyewf`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `image.partitions`

Parse the partition table (MBR and GPT) of a disk image (raw dd or E01) without mounting or modifying it. Pure-Python parser.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `partition_table`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `sector_size` | integer | no | 512 |  |

## linux

### `linux.auth_events`

Extract SSH authentication and sudo events from common offline Linux auth logs (including rotated gzip files).

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `auth_events`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `user` | string | no |  |  |
| `ip` | string | no |  |  |
| `limit` | integer | no | 10000 |  |

### `linux.offline_inventory`

Inventory a mounted/offline Linux root filesystem: OS release, accounts, package logs, web roots and Docker metadata presence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `account_limit` | integer | no | 1000 |  |

### `linux.package_events`

Extract package install/upgrade/remove events from common Debian/RPM/Pacman logs in an offline Linux root.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `package` | string | no |  |  |
| `limit` | integer | no | 5000 |  |

### `linux.persistence_inventory`

Inventory common offline Linux persistence and operator-history locations: cron, systemd overrides, rc.local, SSH authorized_keys and shell histories.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `persistence_candidates`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `max_files` | integer | no | 5000 |  |

## memory

### `memory.handles`

Run the fixed Volatility 3 plugin 'windows.handles' against a memory image and normalise the open handles into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `handles`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

### `memory.malfind`

Run the fixed Volatility 3 plugin 'windows.malfind' against a memory image and normalise the injected/ anomalous memory into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `malfind_hits`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

### `memory.modules`

Run the fixed Volatility 3 plugin 'windows.modules' against a memory image and normalise the kernel modules into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `kernel_modules`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

### `memory.network`

Run the fixed Volatility 3 plugin 'windows.netscan' against a memory image and normalise the network connections into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `network_connections`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

### `memory.processes`

Run the fixed Volatility 3 plugin 'windows.pslist' against a memory image and normalise the process list into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `processes`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

### `memory.volatility_inventory`

Run the fixed Volatility 3 plugin 'windows.info' against a memory image and normalise the system overview into a structured Observation. No arbitrary Volatility args are exposed; the image is read-only evidence.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `system_overview`

Requires: `volatility`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `image` | string | yes |  | EVIDENCE_INPUT |
| `timeout` | integer | no | 300 |  |
| `record_limit` | integer | no | 2000 |  |

## network

### `network.capture_protocols`

Extract bounded DNS questions, plaintext HTTP requests and TLS ClientHello SNI from classic PCAP or PCAPNG.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `dns_queries`, `http_requests`, `tls_sni`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `limit` | integer | no | 5000 |  |

### `network.dns_transactions`

Correlate DNS query and response messages by transaction id and question name, resolving A/AAAA/CNAME answers to their queried names. READ_ONLY.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `dns_transactions`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `limit` | integer | no | 5000 |  |

### `network.flows`

Group captured packets into network flows (TCP conversations and UDP 5-tuples) with packet/byte counts, timestamps and TCP flag summary, without external libraries.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `network_flows`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `max_flows` | integer | no | 500 |  |

### `network.http_sessions`

Reassemble TCP streams and correlate HTTP request/response pairs. When a response body is a file-like object (by content-type or magic), it is extracted to the workspace and registered as a DerivedArtifact, forming the PCAP -> download -> binary analysis chain. STATEFUL: writes only to the workspace.

Safety: `STATEFUL` · Network: `false` · Cost: `high`

Produces: `http_sessions`, `derived_artifacts`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `output_dir` | string | yes |  | WORKSPACE_OUTPUT |
| `packet_limit` | integer | no | 200000 |  |
| `max_sessions` | integer | no | 200 |  |
| `max_body_bytes` | integer | no | 16777216 |  |

### `network.pcap_inventory`

Parse classic PCAP packet headers and summarize IPv4 TCP/UDP endpoint tuples without external libraries.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `sample_limit` | integer | no | 200 |  |

### `network.pcapng_inventory`

Parse PCAPNG interface and enhanced/simple packet blocks and summarize Ethernet IPv4 TCP/UDP flows.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `network_flows`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `sample_limit` | integer | no | 200 |  |

### `network.tcp_reassemble`

Reassemble TCP streams from a capture: per direction it overlays segments by sequence number (handling retransmission, out-of-order and overlap) and emits a hash + bounded hex preview of the logical byte stream. READ_ONLY: the evidence file is never written.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `tcp_streams`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `max_streams` | integer | no | 300 |  |
| `max_stream_bytes` | integer | no | 8388608 |  |

### `network.tls_inventory`

Inventory TLS ClientHello records from a capture: SNI, ALPN, record/client version, supported versions, cipher suites, extensions and a JA3 fingerprint (MD5). READ_ONLY.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `tls_client_hellos`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |
| `limit` | integer | no | 5000 |  |

## recipe

### `recipe.android.appdata_triage`

Inventory extracted Android app data and inspect discovered SQLite databases read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `android_appdata_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `database_limit` | integer | no | 20 |  |

### `recipe.android.deep_static_triage`

Compose APK inventory, binary manifest parsing, signing scheme inventory and targeted DEX searches.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `android_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `extra_query` | string | no |  |  |

### `recipe.android.static_triage`

Compose APK inventory with targeted DEX searches for URLs, crypto API names and storage/network indicators.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `extra_query` | string | no |  |  |

### `recipe.artifact.auto_triage`

Deterministic first-pass routing by artifact magic. This is a convenience baseline; an Agent may choose deeper primitives based on the question.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `recipe.browser.history_triage`

Identify a browser history database and try Chromium and Firefox history parsers read-only.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `browser_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 5000 |  |

### `recipe.database.triage`

Identify and inventory SQLite databases or SQL text dumps without writes/imports.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `database_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `recipe.email.full_offline_triage`

Compose MIME/attachment inventory with offline authentication-context analysis; no DNS/network lookup.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `email_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `recipe.email.offline_triage`

Run offline email authentication-context extraction without DNS or remote lookups.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `recipe.network.capture_triage`

Auto-triage classic PCAP or PCAPNG and extract DNS, HTTP and TLS SNI observations.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `network_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `packet_limit` | integer | no | 200000 |  |

### `recipe.server.deep_offline_triage`

Compose offline Linux inventory, package/auth/persistence, Docker metadata/logs and web configuration/access-log discovery.

Safety: `READ_ONLY` · Network: `false` · Cost: `high`

Produces: `server_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `query` | string | no |  |  |

### `recipe.server.offline_triage`

Compose offline Linux, package-history, Docker and web-config discovery for a mounted server root.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |

### `recipe.timeline.unified`

Build a unified, source-attributed timeline from a filesystem evidence tree and optional extra dftk Observation sources.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `extra_sources` | array | no |  |  |
| `limit` | integer | no | 200000 |  |

### `recipe.wallet.mnemonic_scan`

Scan an extracted evidence tree for checksum-valid BIP39 English mnemonics.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `max_files` | integer | no | 5000 |  |

### `recipe.windows.offline_triage`

Compose offline Windows artifact triage from a SYSTEM Registry hive and/or EVTX file.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `windows_triage`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `system_hive` | string | no |  |  |
| `evtx` | string | no |  |  |

## server

### `server.readonly_inventory`

Run a fixed read-only inventory set over SSH. No arbitrary command parameter is exposed.

Safety: `READ_ONLY` · Network: `true` · Cost: `low`

Produces: `server_inventory`

Requires: `paramiko`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `host` | string | yes |  |  |
| `username` | string | yes |  |  |
| `port` | integer | no | 22 |  |
| `identity_file` | string | no |  |  |
| `password_env` | string | no | DFTK_SSH_PASSWORD |  |
| `timeout` | integer | no | 15 |  |

## timeline

### `timeline.file_metadata`

Create a bounded filesystem metadata timeline from an extracted evidence tree.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `max_files` | integer | no | 50000 |  |
| `limit` | integer | no | 100000 |  |

### `timeline.merge`

Merge time-bearing events from multiple dftk tool outputs or inline sources into one normalized, source-attributed timeline. Inputs are read-only; nothing is modified.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `files` | array | no |  |  |
| `inline` | array | no |  |  |
| `limit` | integer | no | 200000 |  |

## tree

### `tree.inventory`

Bounded inventory of an extracted evidence directory: file counts, extensions, total size and largest files.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `file_inventory`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `max_files` | integer | no | 50000 |  |
| `largest` | integer | no | 100 |  |

## web

### `web.access_log_summary`

Summarize common Nginx/Apache access logs in an offline tree: clients, methods, status codes and requested URIs.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `web_requests`, `web_log_summary`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `limit` | integer | no | 200000 |  |
| `sample_limit` | integer | no | 1000 |  |

### `web.config_candidates`

Discover likely web/application configuration files under an offline directory; optionally extract key names while redacting values.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `observation`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `root` | string | yes |  |  |
| `max_files` | integer | no | 20000 |  |
| `extract_keys` | boolean | no | True |  |

### `web.config_extract`

Parse one explicit configuration file and return key/value structure. Secret-like values are redacted unless include_values=true.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `config_values`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `include_values` | boolean | no | False |  |
| `limit` | integer | no | 1000 |  |

## windows

### `windows.amcache`

Parse Amcache.hve (pure-Python REGF reader) for program/file evidence: file paths, SHA1 hashes, sizes, versions, last-modified timestamps, and the linked ProgramId. Also extracts InventoryApplication program metadata.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `amcache_files`, `amcache_programs`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |

### `windows.evtx_summary`

Summarize EVTX providers, event IDs and timestamps using python-evtx when installed.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `event_log_summary`, `timeline`

Requires: `python-evtx`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 100000 |  |
| `sample_limit` | integer | no | 500 |  |

### `windows.lnk`

Parse a Windows Shell Link (.lnk) shortcut with pure-Python parsing: recover the target path, file attributes, creation/access/write timestamps, and TrackerDataBlock (machine id / MAC).

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `lnk_target`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `windows.mft`

Parse an NTFS $MFT file with pure-Python parsing: recover file/directory paths, Standard Information and $FILE_NAME timestamps, record flags and sizes. Best-effort full-path reconstruction via parent references.

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `mft_records`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `record_limit` | integer | no | 200000 |  |
| `deleted_only` | boolean | no | False |  |

### `windows.prefetch`

Parse a Windows Prefetch file (.pf, versions 17/23/26/30) with pure-Python parsing: recover the executable path, prefetch hash, run count and last-run time(s), and the set of referenced files.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `prefetch_execution`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |

### `windows.recyclebin`

Parse Windows Recycle Bin $I metadata files (Windows 10+): recover the original deleted file name, size and deletion time, and detect the paired $R data file when present.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `recyclebin_deleted`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `find_data` | boolean | no | True |  |

### `windows.registry_deleted_keys`

Recover deleted/unreachable key nodes (nk) from a Windows Registry hive using DFTK's pure-Python parser. Deleted keys remain in the hive as free/unlinked cells; we walk the live tree to learn reachable cells, then scan every cell for an nk signature that is free or unreachable. No external dependency.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `deleted_registry_keys`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `limit` | integer | no | 500 |  |

### `windows.registry_inventory`

Inventory a Windows Registry hive using python-registry when installed; never modifies the hive.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `registry_inventory`

Requires: `python-registry`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `key_limit` | integer | no | 10000 |  |
| `depth` | integer | no | 2 |  |

### `windows.registry_tree`

Parse a Windows Registry hive (REGF) with DFTK's pure-Python parser and return the live key tree (names, LastWrite timestamps, values). No external dependency.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `registry_tree`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `depth` | integer | no | 3 |  |
| `key_limit` | integer | no | 5000 |  |

### `windows.shimcache`

Parse the AppCompatCache (Shimcache) registry blob. Extracts per-entry file paths and last-modified timestamps. Execution is explicitly NOT inferred (execution_inference='unsupported'); correlate with Prefetch/Amcache/MFT/USN.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `shimcache_entries`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `is_hive` | boolean | no | False |  |

### `windows.srum`

Parse SRUDB.dat (ESE database) for application/network resource usage. Requires the 'esedb' package; returns UNSUPPORTED when unavailable. Extracts the well-known usage tables with application, SID, timestamps, and byte/packet counters.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `srum_tables`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  | EVIDENCE_INPUT |
| `table_limit` | integer | no | 64 |  |
| `row_limit` | integer | no | 5000 |  |

### `windows.usb_artifacts`

Extract USBSTOR and MountedDevices artifacts from an offline SYSTEM Registry hive.

Safety: `READ_ONLY` · Network: `false` · Cost: `low`

Produces: `usb_devices`

Requires: `python-registry`

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `system_hive` | string | yes |  |  |

### `windows.usnjrnl`

Parse an NTFS $UsnJrnl $J change-journal stream (pure-Python): recover USN records with File Reference Numbers, timestamps, reason codes, source info and file attributes. Optionally resolves FRNs to full NTFS paths via a provided $MFT. Reports file-system activity factually; it does NOT infer program execution (correlate with Prefetch/Amcache/MFT instead).

Safety: `READ_ONLY` · Network: `false` · Cost: `medium`

Produces: `usn_records`, `timeline`

Requires: none declared

| Parameter | Type | Required | Default | Path role |
|---|---|---|---|---|
| `path` | string | yes |  |  |
| `mft_path` | string | no | None |  |
| `record_limit` | integer | no | 200000 |  |
| `reason_filter` | array | no | None |  |
