# Implementer map

Status: **planned; only the scaffold exists, no product behaviour.** This page maps the boundaries that [PROJECT-PLAN.md](PROJECT-PLAN.md) requires onto a module layout so that parallel tickets do not collide. It adds no requirement; the plan wins where they differ. The names are the orchestrator's proposal, fixed by the scaffold; a ticket that changes one corrects this page in the same pull request.

## Planned module map

| Boundary | Module | Owns | Parent ticket |
|---|---|---|---|
| Contracts | `csv_preflight/contracts.py` | Header, record span, destination schema, validation error, disposition shapes and limits | #2 |
| Dialect scanner | `csv_preflight/dialect.py` | Byte checks, quote and line grammar, spans, agreement with `csv.reader` | #3 |
| Mapping | `csv_preflight/mapping.py` | Versioned header mappings, absent-header errors | #4 |
| Field rules | `csv_preflight/rules.py` | Destination-order checks, normalisation, reason codes | #4 |
| Classification | `csv_preflight/classify.py` | Dispositions, winner links, count equations | #5 |
| Exports | `csv_preflight/exports.py` | Clean CSV, complete and rejects JSONL | #5 |
| Storage | `csv_preflight/store.py` | SQLite schema, run keys, attempts, retention, single-instance lock | #4 (mapping versions), #6 |
| HTTP | `csv_preflight/server.py` | Loopback bind, request guards, routes, static assets | #2 (page), #6 |
| Browser assets | `csv_preflight/static/` | File, Map, Run, Review, Export steps and history | #2 (shell), #6 |
| Fixtures and oracle | `tests/fixtures/` | Fixtures A, B and C as bytes built without the application writer | #2, #3, #5 |

Dependency direction: `server` depends on `store`, `exports` and `classify`; `classify` on `rules`; `rules` and `mapping` on `contracts`; `dialect` on `contracts`. `contracts` imports nothing from the package. Test fixtures import nothing from the package.

## Freeze points

Parallel tickets rely on these shapes. A ticket that changes a frozen shape updates this page and every dependent ticket in the same pull request.

- **Header, record-span, destination schema, validation error and disposition shapes**, with limits: ticket #2 writes them down here before #3 and #4 start in parallel.
- **Parsed-record interface** (ordinal, physical line range, fields): #3 provides it, #4 may start from fixture records of the same shape.
- **Run key fields and audit JSONL schema**: #5 documents them before #6 stores them.

## What is verified where

Python tests run locally and in CI on Linux and Windows. Browser checks are manual in Chrome unless a ticket states a headless run.
