# Owner decisions

A dated record of the decisions made for this repository, so the rules do not depend on anyone's memory of a conversation. Changing any entry needs the owner. An agent that finds a decision blocking a ticket stops and says so.

The owner made decisions 1 to 10 and 12 for all repositories that get the SDLC kit (on 2026-11-22; 4, 5 and 9 changed on 2026-11-27), and asked on 2026-11-24 to apply the kit here (jortega0033/sdlc-kit v1.2.0). Each row says who decided.

| # | Decision | Source | Date | Implemented in |
|---|---|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch (`main`). | decided by the owner | 2026-11-22 | `CLAUDE.md`, `.claude/`, `.github/` |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | decided by the owner | 2026-11-22 | `.claude/agents/`, `.claude/agency-agents/README.md`, `CLAUDE.md` "Agent roles" |
| 3 | Every open ticket is about app implementation; tooling is installed, not ticketed. | decided by the owner | 2026-11-22 | `.claude/`, `.github/`, `docs/` |
| 4 | Agents take tickets to a pull request and merge the small, low-risk ones themselves; anything critical (business, cost, security, dependencies, CI, agent configuration, hard decisions) waits for the owner's review. Only the owner releases. | decided by the owner | 2026-11-27 | `CLAUDE.md` "Merge rule", `.claude/skills/next-ticket/SKILL.md`, `docs/RELEASING.md` |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. Once started, a run goes on ticket after ticket without stopping. | decided by the owner | 2026-11-27 | `.claude/skills/next-ticket/SKILL.md` |
| 6 | A review gate hook blocks opening, readying or merging a pull request until the gate roles have run after the last code edit. | decided by the owner | 2026-11-22 | `.claude/hooks/role_gate.py`, `.claude/settings.json` |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | decided by the owner | 2026-11-22 | `LOOP.md`, `loop-constraints.md`, `loop-budget.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | decided by the owner | 2026-11-22 | `.github/workflows/ci.yml`; branch protection is a repository setting |
| 9 | Permission rules: documented commands and merges are allowed, and nothing asks first, so a started run is not interrupted. Denied: force pushes, pushes to the default branch, merges with `--admin`, `git reset --hard`, `git clean`, deleting the repository, releases and reads of secrets. | decided by the owner | 2026-11-27 | `.claude/settings.json` |
| 10 | Open decisions on tickets are settled with the ticket's stated default; where a ticket states none, the conservative option is taken and flagged in the issue. | decided by the owner | 2026-11-22 | The list below; the issues themselves |
| 11 | Nothing is installed on the owner's PC for this project: Python is already there. No third-party Python package is used, in the application or in tests. | recommended by the orchestrator, following the plan (Python standard library modules, no package install) | 2026-11-24 | `CLAUDE.md` "Commands", `.github/workflows/ci.yml` |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed in the repository and used for UI work and for copy. | decided by the owner | 2026-11-22 | `docs/ui-quality.md`, `.claude/skills/` |
| 13 | Visual system: the Pipenzo Flow look tokens. | decided by the owner | 2026-11-23 | `csv_preflight/static/tokens.css`, `docs/design-tokens.md` |
| 14 | Token rules 14-D1 to 14-D4. | 14-D1 use of yellow decided by the owner; how it is drawn, and 14-D2 to 14-D4, recommended by the orchestrator and adopted under the owner's delegation of 2026-11-23 | 2026-11-23 | `docs/design-tokens.md`; applied in UI tickets |

## Open ticket decisions settled by default (entry 10)

The plan leaves these open. Each is a recommendation by the orchestrator, adopted under entry 10 on 2026-11-24, and holds unless the owner changes it in the issue. None blocks a ticket.

| Issue | Decision | Default |
|---|---|---|
| all | Python versions | 3.12 and 3.13 in CI; the code uses nothing newer than 3.12. |
| #2 | Address and data directory | `http://127.0.0.1:8767`, changed with `--port`; `--data-dir` is required and has no default, as the plan asks for an explicit directory. |
| #2 | Platforms | Linux is the plan's target. Code and tests also run on Windows; the single-instance lock uses `fcntl` or `msvcrt`. |
| #3 | Malformed file after the header | The file is blocked as a whole and the response gives the first error with its line and, where known, record range. |
| #6 | Retention | 128 MiB of source payload and 50 runs. At a limit new work is refused; history is deleted only by an explicit confirmed action. |
| #6 | Review page size | 50 records per page, ordered by ordinal. |
| #7 | Network block in Chrome | Recorded as an owner check with the steps, or a headless run with a blocking host rule; the pull request says which. |
| none | Licence | MIT, already in the repository (`LICENSE`). No ticket changes it. |

## Program decisions (owner, 2026-11-24)

The owner accepted the goal and each suggestion below. They apply from the phase they name; the rules of `CLAUDE.md` hold for phase 1 as written.

| Decision | Implemented in |
|---|---|
| The repository has a program goal above phase 1: a data intake engine that proves what it accepted, in 6 phases. | Program issue #35 |
| Phase 1 reads with the Python csv module next to its own scanner. Suggested: keep that rule; from phase 2 the own reader decides and csv is one of the judges. | Program issue #35 |
| User-defined schemas and other dialects are outside the first release. Suggested: they enter with phases 2 and 4. | Program issue #35 |
| Plain Python may be too slow for 100 GB. Suggested: choose the engine language at the start of phase 6 and keep the file formats and tests. | Program issue #35 |
