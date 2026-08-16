# DFTK 3.3.0 Capability Catalog (verified)

Generated from the live DFTK 3.3.0 capability registry. **72 capabilities** across 20 domains.

All capabilities are read-only / evidence-preserving unless marked `STATEFUL`. `network: true` means the capability may perform outbound lookups (disabled by default on the MCP server).


## Domains

- `android` — 7 capabilities

- `archive` — 2 capabilities

- `artifact` — 1 capabilities

- `binary` — 3 capabilities

- `browser` — 4 capabilities

- `crypto` — 3 capabilities

- `database` — 4 capabilities

- `docker` — 2 capabilities

- `email` — 4 capabilities

- `encoding` — 1 capabilities

- `file` — 4 capabilities

- `image` — 2 capabilities

- `linux` — 4 capabilities

- `network` — 3 capabilities

- `recipe` — 14 capabilities

- `server` — 1 capabilities

- `timeline` — 2 capabilities

- `tree` — 1 capabilities

- `web` — 3 capabilities

- `windows` — 7 capabilities


## android

### `android.apk_endpoints`

Extract URL/domain/IP/content-URI endpoint candidates from parsed DEX strings across an APK with source DEX/string locators.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |

### `android.apk_inventory`

Inventory APK ZIP members, DEX files, native libraries, certificates and manifest presence.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `android.apk_manifest`

Parse AndroidManifest.xml from an APK, including binary AXML, and summarize package, permissions, SDK and components.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `include_elements` | boolean |  |

### `android.apk_search`

Search parsed DEX string tables inside an APK for a literal or regular expression.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `query` | string |  |
| `regex` | boolean |  |
| `limit` | integer |  |

### `android.apk_signing_inventory`

Detect APK v1 signing entries and APK Signing Block scheme IDs (v2/v3/v3.1/source stamp) without modifying the APK.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `android.appdata_inventory`

Inventory an extracted Android app data directory (shared_prefs, databases, files, cache) without modifying it.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `max_files` | integer |  |

### `android.dex_strings`

Parse the DEX string table using ULEB128 string_data_item and modified UTF-8.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `contains` | string |  |
| `regex` | string |  |
| `limit` | integer |  |


## archive

### `archive.extract_safe`  _(safety=STATEFUL)_

Extract ZIP/TAR members into a separate workspace with path-traversal, member-count and total-size limits. Source archive is never modified.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `output_dir` | string |  |
| `member_limit` | integer |  |
| `total_size_limit` | integer |  |
| `overwrite` | boolean |  |

### `archive.inventory`

Inventory ZIP/TAR archive members and metadata without extraction. The member list is bounded by `limit` (peak memory stays proportional to `limit` even for very large archives).


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |


## artifact

### `artifact.inspect`

Identify an artifact from magic bytes and container structure, with size and SHA-256.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |


## binary

### `binary.elf_inventory`

Parse ELF architecture and section metadata; optionally extract bounded printable strings.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `strings` | boolean |  |
| `string_limit` | integer |  |

### `binary.native_indicator_scan`

Heuristically scan a native binary for JNI names, crypto APIs, URLs and suspicious command/network indicators. Findings are indicators, not conclusions.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |

### `binary.pe_inventory`

Parse PE/COFF architecture, timestamp, characteristics and section table without executing the binary.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `strings` | boolean |  |
| `string_limit` | integer |  |


## browser

### `browser.chromium_cookies`

Inventory Chromium/Chrome/Edge Cookies SQLite metadata in immutable read-only mode. Plaintext values are omitted unless include_values=true; encrypted blobs are never decrypted.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `include_values` | boolean |  |
| `limit` | integer |  |

### `browser.chromium_downloads`

Read Chromium/Chrome/Edge download records and URL chains from History SQLite in immutable read-only mode.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |

### `browser.chromium_history`

Read Chromium/Chrome/Edge History SQLite visits and URLs in immutable read-only mode.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |

### `browser.firefox_history`

Read Firefox places.sqlite history visits in immutable read-only mode.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |


## crypto

### `crypto.bip39_scan`

Scan one file or directory for BIP39 English word sequences and distinguish checksum-valid mnemonics.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `max_files` | integer |  |
| `max_bytes_per_file` | integer |  |
| `max_candidates` | integer |  |

### `crypto.bip39_validate`

Validate a BIP39 English mnemonic including its checksum.


**Parameters**

| name | type | description |
|------|------|-------------|
| `mnemonic` | string |  |

### `crypto.entropy_profile`

Compute bounded Shannon entropy per file block to highlight compressed/encrypted/high-entropy regions; does not classify encryption by itself.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `block_size` | integer |  |
| `block_limit` | integer |  |


## database

### `database.sql_dump_inventory`

Inventory generic SQL text dumps (MySQL/PostgreSQL/SQLite-style) for databases, CREATE TABLE statements and INSERT counts without importing the dump.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `max_bytes` | integer |  |
| `statement_limit` | integer |  |

### `database.sqlite_inventory`

Open SQLite in read-only URI mode and report objects, schemas and optional row counts.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `count_rows` | boolean |  |
| `table_limit` | integer |  |

### `database.sqlite_query`

Execute one bounded read-only SELECT/WITH query against SQLite with SQLite authorizer write operations denied.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `sql` | string |  |
| `params` | array |  |
| `limit` | integer |  |

### `database.sqlite_search`

Search bounded SQLite tables/columns for a literal value using immutable read-only access; avoids requiring the Agent to construct schema-specific SQL first.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `query` | string |  |
| `case_sensitive` | boolean |  |
| `table_limit` | integer |  |
| `column_limit` | integer |  |
| `result_limit` | integer |  |


## docker

### `docker.offline_inventory`

Recover Docker container configuration from an offline /var/lib/docker tree without starting Docker.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `limit` | integer |  |

### `docker.offline_logs`

Read bounded Docker json-file container logs from an offline Docker data root, optionally filtering for a literal query.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `query` | string |  |
| `limit` | integer |  |


## email

### `email.auth_analyze`

Offline EML analysis of sender headers, DKIM identifiers and Authentication-Results. Header mismatches are context, not automatic spoofing verdicts.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `email.dkim_verify`  _(network; requires=dkimpy,dnspython)_

Verify DKIM signatures using dkimpy and DNS. This is signature verification, not DKIM-Signature repair.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `email.mime_inventory`

Parse an RFC-style email file and inventory headers, MIME parts and attachment hashes without extracting or executing content.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `include_body_preview` | boolean |  |
| `preview_chars` | integer |  |

### `email.spf_verify`  _(network; requires=pyspf,dnspython)_

Evaluate SPF for a supplied sending IP and SMTP envelope identity using pyspf and DNS; it does not infer IP from From headers.


**Parameters**

| name | type | description |
|------|------|-------------|
| `ip` | string |  |
| `mail_from` | string |  |
| `helo` | string |  |


## encoding

### `encoding.decode_candidates`

Try common reversible text encodings (hex, Base64/Base64URL, percent-encoding) and return bounded decoded candidates with printable ratios.


**Parameters**

| name | type | description |
|------|------|-------------|
| `value` | string |  |
| `max_output_bytes` | integer |  |


## file

### `file.hash`

Compute cryptographic hashes of one file without modifying it.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `algorithms` | array |  |

### `file.search_tree`

Search a file or directory tree for text/byte patterns with bounded results and source locators.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `query` | string |  |
| `regex` | boolean |  |
| `case_sensitive` | boolean |  |
| `max_files` | integer |  |
| `max_file_size` | integer |  |
| `limit` | integer |  |

### `file.strings`

Extract bounded printable ASCII strings with byte offsets.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `min_length` | integer |  |
| `limit` | integer |  |

### `file.strings_unicode`

Extract bounded UTF-16LE/UTF-16BE printable strings with byte offsets; useful for Windows/native artifacts that ASCII strings miss.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `min_length` | integer |  |
| `limit` | integer |  |


## image

### `image.e01_filesystem_inventory`  _(requires=pyewf,pytsk3)_

Read E01/EWF through pyewf + pytsk3 and inventory volume partitions and bounded filesystem root entries without mounting or modifying evidence.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `entry_limit` | integer |  |

### `image.e01_inventory`  _(requires=pyewf)_

Open an E01/EWF image read-only with pyewf and report segment/media metadata. Filesystem traversal is intentionally a separate future primitive.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |


## linux

### `linux.auth_events`

Extract SSH authentication and sudo events from common offline Linux auth logs (including rotated gzip files).


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `user` | string |  |
| `ip` | string |  |
| `limit` | integer |  |

### `linux.offline_inventory`

Inventory a mounted/offline Linux root filesystem: OS release, accounts, package logs, web roots and Docker metadata presence.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `account_limit` | integer |  |

### `linux.package_events`

Extract package install/upgrade/remove events from common Debian/RPM/Pacman logs in an offline Linux root.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `package` | string |  |
| `limit` | integer |  |

### `linux.persistence_inventory`

Inventory common offline Linux persistence and operator-history locations: cron, systemd overrides, rc.local, SSH authorized_keys and shell histories.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `max_files` | integer |  |


## network

### `network.capture_protocols`

Extract bounded DNS questions, plaintext HTTP requests and TLS ClientHello SNI from classic PCAP or PCAPNG.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `packet_limit` | integer |  |
| `limit` | integer |  |

### `network.pcap_inventory`

Parse classic PCAP packet headers and summarize IPv4 TCP/UDP endpoint tuples without external libraries.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `packet_limit` | integer |  |
| `sample_limit` | integer |  |

### `network.pcapng_inventory`

Parse PCAPNG interface and enhanced/simple packet blocks and summarize Ethernet IPv4 TCP/UDP flows.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `packet_limit` | integer |  |
| `sample_limit` | integer |  |


## recipe

### `recipe.android.appdata_triage`

Inventory extracted Android app data and inspect discovered SQLite databases read-only.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `database_limit` | integer |  |

### `recipe.android.deep_static_triage`

Compose APK inventory, binary manifest parsing, signing scheme inventory and targeted DEX searches.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `extra_query` | string |  |

### `recipe.android.static_triage`

Compose APK inventory with targeted DEX searches for URLs, crypto API names and storage/network indicators.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `extra_query` | string |  |

### `recipe.artifact.auto_triage`

Deterministic first-pass routing by artifact magic. This is a convenience baseline; an Agent may choose deeper primitives based on the question.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `recipe.browser.history_triage`

Identify a browser history database and try Chromium and Firefox history parsers read-only.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |

### `recipe.database.triage`

Identify and inventory SQLite databases or SQL text dumps without writes/imports.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `recipe.email.full_offline_triage`

Compose MIME/attachment inventory with offline authentication-context analysis; no DNS/network lookup.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `recipe.email.offline_triage`

Run offline email authentication-context extraction without DNS or remote lookups.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `recipe.network.capture_triage`

Auto-triage classic PCAP or PCAPNG and extract DNS, HTTP and TLS SNI observations.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `packet_limit` | integer |  |

### `recipe.server.deep_offline_triage`

Compose offline Linux inventory, package/auth/persistence, Docker metadata/logs and web configuration/access-log discovery.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `query` | string |  |

### `recipe.server.offline_triage`

Compose offline Linux, package-history, Docker and web-config discovery for a mounted server root.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |

### `recipe.timeline.unified`

Build a unified, source-attributed timeline from a filesystem evidence tree and optional extra dftk Observation sources.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `extra_sources` | array | Optional paths to dftk Observation JSON files to merge in |
| `limit` | integer |  |

### `recipe.wallet.mnemonic_scan`

Scan an extracted evidence tree for checksum-valid BIP39 English mnemonics.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `max_files` | integer |  |

### `recipe.windows.offline_triage`

Compose offline Windows artifact triage from a SYSTEM Registry hive and/or EVTX file.


**Parameters**

| name | type | description |
|------|------|-------------|
| `system_hive` | string |  |
| `evtx` | string |  |


## server

### `server.readonly_inventory`  _(network; requires=paramiko)_

Run a fixed read-only inventory set over SSH. No arbitrary command parameter is exposed.


**Parameters**

| name | type | description |
|------|------|-------------|
| `host` | string |  |
| `username` | string |  |
| `port` | integer |  |
| `identity_file` | string |  |
| `password_env` | string |  |
| `timeout` | integer |  |


## timeline

### `timeline.file_metadata`

Create a bounded filesystem metadata timeline from an extracted evidence tree.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `max_files` | integer |  |
| `limit` | integer |  |

### `timeline.merge`

Merge time-bearing events from multiple dftk tool outputs or inline sources into one normalized, source-attributed timeline. Inputs are read-only; nothing is modified.


**Parameters**

| name | type | description |
|------|------|-------------|
| `files` | array | Paths to dftk Observation JSON files (each should contain facts.events) |
| `inline` | array | Inline sources: {"source": label, "events": [...]} bundles or flat events with a 'source' key |
| `limit` | integer |  |


## tree

### `tree.inventory`

Bounded inventory of an extracted evidence directory: file counts, extensions, total size and largest files.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `max_files` | integer |  |
| `largest` | integer |  |


## web

### `web.access_log_summary`

Summarize common Nginx/Apache access logs in an offline tree: clients, methods, status codes and requested URIs.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `limit` | integer |  |
| `sample_limit` | integer |  |

### `web.config_candidates`

Discover likely web/application configuration files under an offline directory; optionally extract key names while redacting values.


**Parameters**

| name | type | description |
|------|------|-------------|
| `root` | string |  |
| `max_files` | integer |  |
| `extract_keys` | boolean |  |

### `web.config_extract`

Parse one explicit configuration file and return key/value structure. Secret-like values are redacted unless include_values=true.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `include_values` | boolean |  |
| `limit` | integer |  |


## windows

### `windows.evtx_summary`  _(requires=python-evtx)_

Summarize EVTX providers, event IDs and timestamps using python-evtx when installed.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `limit` | integer |  |
| `sample_limit` | integer |  |

### `windows.lnk`

Parse a Windows Shell Link (.lnk) shortcut with pure-Python parsing: recover the target path, file attributes, creation/access/write timestamps, and TrackerDataBlock (machine id / MAC).


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `windows.mft`

Parse an NTFS $MFT file with pure-Python parsing: recover file/directory paths, Standard Information and $FILE_NAME timestamps, record flags and sizes. Best-effort full-path reconstruction via parent references.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `record_limit` | integer |  |
| `deleted_only` | boolean |  |

### `windows.prefetch`

Parse a Windows Prefetch file (.pf, versions 17/23/26/30) with pure-Python parsing: recover the executable path, prefetch hash, run count and last-run time(s), and the set of referenced files.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |

### `windows.recyclebin`

Parse Windows Recycle Bin $I metadata files (Windows 10+): recover the original deleted file name, size and deletion time, and detect the paired $R data file when present.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `find_data` | boolean |  |

### `windows.registry_inventory`  _(requires=python-registry)_

Inventory a Windows Registry hive using python-registry when installed; never modifies the hive.


**Parameters**

| name | type | description |
|------|------|-------------|
| `path` | string |  |
| `key_limit` | integer |  |
| `depth` | integer |  |

### `windows.usb_artifacts`  _(requires=python-registry)_

Extract USBSTOR and MountedDevices artifacts from an offline SYSTEM Registry hive.


**Parameters**

| name | type | description |
|------|------|-------------|
| `system_hive` | string |  |
