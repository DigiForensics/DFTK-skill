# Browser artifacts

## Choose the native source

| Evidence | Capability | What it establishes |
|---|---|---|
| Chromium/Chrome/Edge `History` | `browser.chromium_history` | Recorded URLs and visits |
| Chromium `History` | `browser.chromium_downloads` | Download records and URL chains |
| Chromium `History`, `keyword_search_terms` | `browser.chromium_search_terms` | Stored keyword search terms with URL context |
| Chromium `Bookmarks` / `Bookmarks.bak` | `browser.chromium_bookmarks` | Bookmark/folder tree, GUIDs and stored dates |
| Chromium `Cookies` | `browser.chromium_cookies` | Cookie metadata; encrypted values are not decrypted |
| Firefox `places.sqlite` | `browser.firefox_history` | Recorded visits |
| Firefox `places.sqlite` | `browser.firefox_bookmarks` | Bookmark/folder/separator records and parent relationships |
| Firefox `cookies.sqlite` | `browser.firefox_cookies` | Cookie metadata, origin attributes and stored dates |

Use live discovery (`dftk_suggest` / `dftk_search_capabilities`) and describe the
selected capability before executing. Older DFTK installations can lack the new
bookmark, Firefox-cookie and keyword-search tools; use the installed registry as
capacity evidence instead of assuming this documentation is executable.

## Bounded investigation

```bash
dftk suggest Bookmarks
dftk run browser.chromium_bookmarks --params '{"path":"Bookmarks","limit":5000}'
dftk run browser.firefox_bookmarks --params '{"path":"places.sqlite","limit":5000}'
dftk run browser.firefox_cookies --params '{"path":"cookies.sqlite","limit":5000}'
dftk run browser.chromium_search_terms --params '{"path":"History","limit":5000}'
```

Persist these runs in one case when correlating sources. Bookmark and Firefox
cookie Observations expose `facts.events` for CaseSession/timeline.merge, along
with record locators and source SHA-256. The search-term tool does not create a
search event from a URL's last-visit time.

Cookie plaintext values are hidden by default. Request `include_values=true`
only when the investigation needs them; do not include secrets in a report just
because they are available. Missing value columns are marked by
`value_column_present=false`, not interpreted as an empty cookie value.

The new SQLite readers use immutable main-database views. A `-wal` or `-journal`
sidecar produces a `partial` warning because pending state is excluded. Preserve
the database and sidecars together; use `database.sqlite_wal` or a separately
prepared derived snapshot when current/WAL state matters. An empty main-database
result with excluded sidecars does not establish absence across the acquisition.

Row limits are 1–100000; queries also have an instruction budget. Text/blob fields
are bounded to 16384 characters/bytes. The Chromium JSON reader defaults to 32 MiB
and depth 64 (configurable up to 128 MiB/depth 128). Its `limit` bounds scanned
nodes, including folders and malformed nodes; it counts folders as records.
`returned_count` is the returned set size, not the total number in the source.
Limits, invalid dates, malformed nodes, ancestry cycles and missing parents
produce `partial` results with warnings. Source read/parse failures are `error`;
missing required tables/columns and unknown bookmark formats are `unsupported`.
The Chromium file's embedded bookmark checksum is not verified.

## Interpret only the stored facts

A bookmark can be imported or synchronized; its addition date does not establish
a page visit. A cookie record does not prove a successful authenticated action or
identify the person using the profile. `originAttributes` preserve Firefox
container/partition context; do not merge cookie identities on host/name alone.
A keyword-search record is recorded context, not proof that an external search
completed. `url_last_visit_time` belongs to the URL record and is not an exact
search timestamp. Corroborate attribution using another source.

## Format references

The parsers follow upstream field definitions:

- [Chromium bookmark codec](https://raw.githubusercontent.com/chromium/chromium/main/components/bookmarks/browser/bookmark_codec.cc)
- [Chromium keyword-search schema](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/history/core/browser/url_database.cc)
- [Firefox Places tables](https://raw.githubusercontent.com/mozilla/gecko-dev/master/toolkit/components/places/nsPlacesTables.h)
- [Firefox persistent cookie schema](https://raw.githubusercontent.com/mozilla/gecko-dev/master/netwerk/cookie/CookiePersistentStorage.cpp)
