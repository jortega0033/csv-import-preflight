# CSV Import Preflight

An offline workbench for mapping, validating and reconciling CSV imports.

This repository contains the plan for the first implementation epic and an empty runnable scaffold. There is no product behaviour yet.

- [Product requirements](docs/PROJECT-PLAN.md#product-requirements)
- [Technical design](docs/PROJECT-PLAN.md#technical-design)
- [Epic and implementation tickets](https://github.com/jortega0033/csv-import-preflight/issues)

The first plan of phase 1 said 16–23 engineering hours. Its open tickets, with tests and review, add up to 54 to 80 hours; the whole program is larger and is described below. All figures are estimates.

Licensed under the [MIT License](LICENSE).

## Program goal

Turn the preflight into a complete intake engine for messy tabular files: own detection of encodings and dialects, own readers for delimited, fixed-width and spreadsheet formats, a compiled rule language, matching of records across deliveries, and files far larger than memory, with no CSV, spreadsheet, XML, dataframe or rule library in the engine.

The program is planned ([#35](https://github.com/jortega0033/csv-import-preflight/issues/35)). Phase 1 is the current epic [#1](https://github.com/jortega0033/csv-import-preflight/issues/1) and the only phase with tickets.

**Score.** Share of files in an annotated public corpus of messy tables that load with the right dialect and the right value in every cell, next to the same figure for two existing loaders.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 54 to 80 | [#1](https://github.com/jortega0033/csv-import-preflight/issues/1) |
| 2 | Dialects and encodings | 110 to 190 | [#36](https://github.com/jortega0033/csv-import-preflight/issues/36) |
| 3 | File formats | 150 to 260 | [#37](https://github.com/jortega0033/csv-import-preflight/issues/37) |
| 4 | Rule language and compiler | 130 to 230 | [#38](https://github.com/jortega0033/csv-import-preflight/issues/38) |
| 5 | Records across deliveries | 120 to 210 | [#39](https://github.com/jortega0033/csv-import-preflight/issues/39) |
| 6 | Files larger than memory | 130 to 220 | [#40](https://github.com/jortega0033/csv-import-preflight/issues/40) |

About 690 to 1190 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.
