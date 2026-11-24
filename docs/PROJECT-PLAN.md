# CSV Import Preflight

The example source, destination schema and supplier file are fictional. An actual source workflow and target format are product decisions before using this design with another system.

## Product requirements

### User and outcome

A small operations team receives supplier catalog CSVs that vary in header names, column order, date or number conventions, and record quality. The first release targets a bounded parts catalog with four destination fields. An operator can load a file, preview records, assign source columns, run validation, reconcile every logical record, and download a clean import and a separate record audit. A saved mapping can be pinned and applied to the next weekly file.

**First useful result.** From a fresh offline browser, open the bundled supplier file, map its four required columns, review the reasons for exclusion, and download the accepted part records without editing the original input. Reopen the result from history after an app restart.

| Requirement | Observable outcome |
| --- | --- |
| PR-01 Input confidence | See the original file size, exact header names, first valid preview records, and physical source lines. A format failure gives a location and reason. |
| PR-02 Repeatable mapping | Map source headers to destination fields once and save a version with all rules. A reorder of matching source columns works without changing the mapping. |
| PR-03 Reviewable validation | Inspect accepted, invalid and duplicate outcomes with deterministic reason codes and original identifiers or records. |
| PR-04 Reconciled export | Download accepted rows and a complete record audit with stable order. Match source record count against the three dispositions. |
| PR-05 Durable runs | Retrieve a completed run after restart, retry an interrupted run and keep older results pinned to their original rules. |
| PR-06 Local use | Complete the workflow with network access disabled except loopback. Use visible status, labeled keyboard controls and text as well as color for errors. |

The first release includes one explicit UTF-8 comma dialect, one destination schema, reusable versions of header mappings, one documented duplicate policy and a last-completed run view. Later increments can add a reviewed semicolon dialect, cross-file reference joins, and user-defined schemas. Live catalog integrations, external data stores, automatic encoding detection, real supplier data, and direct import to third-party systems are outside this release. A first preview proves the input path. The full delivery requires at least one completed export and restart verified against independent expected data.

## Technical design

### Runtime and interaction

Use Python 3.12 standard library HTTP, CSV, JSON, hashlib and sqlite3 modules and static HTML, CSS and JavaScript in Chrome. Launch the server with a loopback address and an explicit user-owned data directory. Record installed versions, test sqlite3 availability, and stage the bundled fixture before starting offline. Normal use needs no build tool, package install, CDN, account, network provider or browser extension. Enforce one app instance per local database directory using a Linux process lock released by process exit. Use synthetic fixtures only.

The UI sequence is File → Map → Run → Review → Export. Show the source and total on each step. Keep native labels and report focus assignment when an action fails. Show current status in text, distinguish a pending operation from a format error, and retain an unsaved mapping when a stale save is rejected. The review table paginates by record ordinal and filters by disposition. It renders original field text through DOM text nodes. It gives line ranges for records that cover multiple physical lines.

| Entry point | Contract |
| --- | --- |
| POST /api/uploads | The request body is the raw byte stream. Return a stable handle, SHA-256, validated header, preview and logical record count, or a format error. |
| POST /api/mappings | Save a new immutable mapping version using a base version. Reject stale base versions while retaining the local draft. |
| POST /api/runs | Submit one uploaded file and one exact saved mapping version. Return an existing matching run or start one attempt. |
| GET /api/runs/{id} | Return immutable run context, status, summary counts and structured errors. |
| GET /api/runs/{id}/records | Return ordered, filtered pages with ordinal, physical line range and decision evidence. |
| GET /api/runs/{id}/exports/{kind} | Serve the clean CSV or complete JSONL audit from a completed run. |

Use a bounded request body, typed errors with an actionable field or source range, and stable default order. Require the exact local origin for browser writes and content type per endpoint. Use content-disposition download with server-generated filenames. File paths and input headers do not become SQL identifiers or HTML.

### Input dialect and record identity

Treat the source as bytes. Reject empty files, invalid UTF-8, NUL and more than 8 MiB. Allow exactly one optional UTF-8 BOM at the file start, and reject BOM elsewhere. Outside quoted fields accept CRLF or LF as a record terminator and allow a final record without a terminator. A lone CR is an error outside quotes. Within a quoted field preserve embedded CRLF or LF and reject bare CR. Only comma separates fields. Quotes are allowed around an entire field, doubled quotes encode one literal quote, and any other quote or text after a closing quote is a format error. Do not ignore spaces before or after an unquoted field. Do not infer the delimiter from sample data. Count physical lines from one and logical data-record ordinals from one, excluding the header. A blank physical line outside quotes counts as one zero-field record and becomes invalid width. A final terminator alone does not create an extra record.

Use a bounded validation and span pass for the explicit quote and line grammar, then Python csv.reader in the matching configuration with strict mode and untranslated newlines. Reconcile scanner record boundaries with csv.reader output and fail closed on a disagreement. Cap headers at 32 columns, field width at 16,384 characters and data at 20,000 records. A file with malformed quote structure, invalid encoding, missing header, empty or duplicate header names, or a limit violation is blocked as a whole. A well-formed data record with a width different from its header is a row-level invalid result. Header names match case-sensitively with no normalization. [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180.html#section-2) · [Python csv](https://docs.python.org/3.12/library/csv.html)

### Mapping and decision rules

Require exactly one different source header for each field. Extra source columns stay in the record audit. A saved mapping checks all referenced names against a new upload by exact match. If any is absent, block the run and identify the missing name. Reordering and extra columns are permitted. Pin rule and destination schema versions as well as the source mapping to each run.

| Destination | Validation and normalization |
| --- | --- |
| part_id | Trim ASCII spaces at the edges and uppercase ASCII letters. Match an initial ASCII letter followed by 1–19 ASCII letters, digits or hyphens. Empty and malformed inputs have separate codes. |
| label | Preserve UTF-8 text and embedded line breaks. Require a non-whitespace label of at most 80 Unicode code points. Block leading control characters and first non-space formula prefixes such as equals, plus, minus and at-sign with UNSAFE_LABEL_PREFIX. Internal LF and CRLF are valid. |
| quantity | After trimming ASCII spaces, require ASCII digits and parse base ten. Accept zero through 99,999. A blank, signed, decimal or nonnumeric value fails. Canonical export is decimal with no leading zeros. |
| active | After trimming ASCII spaces and lowercasing ASCII letters, accept yes or no. Canonical export is true or false. |

Apply the width check first, then field rules in destination order. Retain all field codes for a record with one or more validation errors. Only fully valid candidates enter duplicate detection. First valid occurrence of a normalized part_id wins in file order. Subsequent valid candidates with that key become duplicate and cite the winning ordinal. An invalid row never claims a key. Every parsed record gets exactly one terminal disposition selected in precedence order invalid, duplicate, accepted. Do not silently repair a cell or overwrite the winning row. The review panel explains how to edit and re-upload a source copy for row changes.

### Persistence and export

Store immutable source bytes and hash in uploads, a template ID and immutable configuration in mapping_versions, one row per exact run key in runs, and one row per ordinal in run_records. Store physical line range, original fields, normalized values if available, disposition and reason codes. Record the winner reference for duplicates. Enable foreign keys per SQLite connection. Retain only files selected locally for this workflow. Use bounded data storage, including a configured 128 MiB source payload budget and a 50-run retained-result cap. When full, stop admitting new work and allow explicit deletion of history with confirmation. Refuse deletion of inputs or mapping versions referenced by retained runs. Distinguish deletion from classification and reprocessing.

Hash raw source bytes, then derive a run key from canonical, length-delimited fields covering file hash, mapping version ID, dialect version, rules version and destination schema version. Unique run key and a write transaction coalesce two matching browser submissions. A duplicate request for an in-flight run returns its current status. Analysis writes final decisions and changes the status to complete in one transaction. Do not expose records or export for incomplete runs. On startup mark a previously running attempt as interrupted. Retry the same run key with an incremented attempt number. Output identity excludes timestamps and attempt number so a retry of equivalent data and policy yields the same decision bytes. Changing rules or source data yields a different run key. Use one worker, individual SQLite connections and a bounded busy timeout with a retryable error. [SQLite transactions](https://www.sqlite.org/lang_transaction.html) · [Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html#transaction-control)

The clean artifact is UTF-8 without BOM and uses the destination header part_id,label,quantity,active in that order. Use a CSV writer with comma, double-quote escaping, and CRLF separators. Preserve values and order from accepted rows. The complete audit is UTF-8 JSON Lines in original ordinal order with original fields, line span, normalized values when present, decision and all reasons. The UI can export a rejects-only JSONL with the same schema. A manifest in the review view shows file hash, mapping version, rule version, accepted, invalid, duplicate and total. Show and verify both equations on complete runs.

- Total logical data records = accepted + invalid + duplicate.
- Clean CSV data records = accepted, and rejects-only records = invalid + duplicate.

## Original verification fixtures

### Fixture A · Weekly supplier file

The original fixture is authored from the table below. Its first three bytes are an optional UTF-8 BOM, record separators are CRLF, and its header is SupplierCode,Product,OnHand,Enabled. Row 3 is quoted, doubles the embedded quotes around Large and contains an actual CRLF before Keep dry. Rows 2 and 4 quote labels containing commas. The test should construct the bytes independently of the app writer.

| Ordinal | Source lines | SupplierCode | Product | OnHand | Enabled | Expected |
| --- | ---: | --- | --- | --- | --- | --- |
| 1 | 2 | A100 | Green bin | 12 | yes | Accepted |
| 2 | 3 | A200 | Bolt, zinc | 003 | YES | Accepted |
| 3 | 4–5 | A300 | Label "Large" followed by a CRLF and Keep dry | 0 | no | Accepted |
| 4 | 6 | a200 | Bolt, new zinc | 4 | yes | Duplicate of ordinal 2 |
| 5 | 7 | A400 | Washer | fox | yes | Invalid quantity |
| 6 | 8 | Empty field | Pin | 5 | yes | Missing part ID |
| 7 | 9 | A500 | Tray | 10 | maybe | Invalid active |
| 8 | 10 | A100 | Green bin | -1 | yes | Invalid quantity |
| 9 | 11 | A600 | Clip | 2 | Field omitted | Invalid width |
| 10 | 12 | A700 | =2+2 | 1 | yes | Invalid label prefix |

The expected clean keys in order are A100, A200, A300, with quantity and active pairs (12, true), (3, true), (0, false). Clean round-trip preserves row 2's comma and row 3's quote and CRLF. The complete audit has exactly ordinals 1–10 and the rejects-only audit has ordinals 4–10. Counts are accepted 3, duplicate 1, invalid 6 and total 10. Duplicate ordinal 4 points to 2. The source maximum line is 12. A clean-file reparse with an independent reader must produce four header fields and three data records.

### Fixture B · Template reuse and precedence

Use LF, no BOM and no final newline. Reorder Enabled,OnHand,Product,SupplierCode,Ignored. Include A200 first with an invalid quantity, then A200 with valid data. Expect first invalid and second accepted in both old and reordered headers with the matching data shape. The optional Ignored field stays in the audit. Remove Enabled in a separate run and expect a named missing-header block with no exports. Save two mappings from the same base version in separate tabs, expect one accepted save and one stale response retaining the stale draft.

### Fixture C · Failure and replay

Provide an unterminated quoted multiline field, a raw non-UTF-8 byte, an unquoted bare quote, a repeated header name and an oversized upload separately. Expect a typed failure with a source range where parseable and no completed result. Add a blank line between two valid data records and expect a single invalid-width record. With Fixture A, inject an interruption after some uncommitted decisions are written, reopen, retry and compare output bytes to the uninterrupted run. From two browser tabs request the same file and mapping version. Verify the same run identifier, completed output or shared pending status, and no duplicate stored decisions. Exact results listed here are expected, pending implementation.

## Epic · Reconcile a reusable supplier import offline

Give an operator a repeatable path from a local supplier file to a validated import with traceable row accounting. Release requires all six tickets, offline browser traversal, a completed retry and restart proof, and exact status counts. The estimated implementation and verification effort is **16–23 engineering hours** across several sessions. The first intake contract comes first. CI-02 and CI-03 can proceed in parallel with fixed parser and schema interfaces. CI-04 integrates both lanes, CI-05 connects durability and the browser journey, and CI-06 closes the release gate.

### CI-01 · Define the import contract and initial local preview

**Estimate.** 2–3 hours. **Dependencies.** None.

As an operator, I can open the local workbench and see an original fixture available without a network connection.

- CI-01-A. Publish typed header, record-span, destination schema, validation error and disposition interfaces with documented limits.
- CI-01-B. Serve a keyboard-accessible static page on loopback and show fixture name and size using a disposable local run. Record the offline entry point and version checks.

### CI-02 · Parse bounded CSV records with exact source locations

**Estimate.** 3–4 hours. **Dependencies.** CI-01.

As an operator, I can distinguish a malformed source file from an individual invalid record.

- CI-02-A. Implement explicit UTF-8 and quote grammar rules, exact header checks and bounded row/field scanning. Validate input bytes before advertising a complete preview.
- CI-02-B. Reproduce Fixture A's logical record and physical line coordinates. Exercise Fixture C's malformed quote, invalid bytes, duplicate header, blank row, size cap and bare CR variants.

### CI-03 · Save and apply versioned mappings and field rules

**Estimate.** 3–4 hours. **Dependencies.** CI-01.

As an operator, I can reuse a mapping after column order changes and see the exact reason a mapped value fails.

- CI-03-A. Apply deterministic required-field and format checks in destination order using parsed records from the agreed interface. Preserve lossless labels and retained extra columns.
- CI-03-B. Verify mapping order independence and absent-header errors from Fixture B. Save two updates using one base version and demonstrate a single successful update. Check first/last accepted quantity boundaries, canonical formatting and unsafe-label tests.

### CI-04 · Classify records and generate reconciled exports

**Estimate.** 2–3 hours. **Dependencies.** CI-02 and CI-03.

As an operator, I can identify what happened to every row and carry the accepted rows into the next step.

- CI-04-A. Apply invalid-before-duplicate precedence and stable winner linking. Check Fixture A totals and Fixture B where an invalid row never claims the key.
- CI-04-B. Generate clean CSV and JSONL audit/rejects deterministically. Verify both count equations, exact winning keys and escaping with an independently authored expected result.

### CI-05 · Finish the browser workflow and durable run history

**Estimate.** 4–6 hours. **Dependencies.** CI-04.

As an operator, I can run a saved mapping, navigate the decision report, and retrieve the same completed export after restart.

- CI-05-A. Wire File → Map → Run → Review → Export. Confirm keyboard access, visible errors, stale-draft retention, paginated reasons and downloadable artifacts.
- CI-05-B. Store snapshots and decisions transactionally. Test concurrent identical submissions, atomic publication and explicit retention limits. Verify old results still reference the correct version after new mapping edits.

### CI-06 · Prove an offline import, restart and recovery

**Estimate.** 2–3 hours. **Dependencies.** CI-05.

As a reviewer, I can reproduce the final workflow using only bundled synthetic inputs.

- CI-06-A. Use an empty temporary data directory and a browser with outbound network blocked. Perform an import and independently open both artifacts. Verify exact accepted values and rejection reasons. Record commands, environment and results.
- CI-06-B. Exercise interruption, retry and restart from Fixture C. Compare clean and audit bytes against the uninterrupted result and recheck both count equations. Record any unverified environment or malformed-input limitation.
