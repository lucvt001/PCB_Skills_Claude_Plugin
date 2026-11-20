---
name: workflow
description: Load first in every session. Human-centric working principles (collaboration, checkpoints, designer/reviewer agents, evidence tags, decisions) plus, for KiCad + JLCPCB PCB projects, the session map and which skills to use.
---

# Workflow

Speed and token savings first; the human drives. Part 1: any engineering project. Part 2: KiCad + JLCPCB PCB projects.

# Part 1: Principles

## Collaboration

- Edit only what was asked; flag anything else, don't fix it unasked.
- Re-read a file before touching it. If it differs from your last copy, it's the user's deliberate change: never revert or "tidy" it; say so if it looks wrong.
- **KiCad open is not a blocker:** edit the project files on disk even if KiCad has them open; don't ask the user to close it and don't wait. When the edits are done, remind the user: **close KiCad without saving** (saving or applying anything from the open session would overwrite the disk edits; unsaved work in that session is lost), then reopen the project to see the changes.
- **Schematic and datasheet-reading stage only:** ask about every choice that changes the result (part options, connector types); decide small details yourself. In later stages (sourcing, layout, release) follow `DECISIONS.md`, `board-defaults.md`, and the stage's rules; ask only where they're silent or conflict.
- Don't commit or push unless asked.

## Checkpoints, no automatic review

- Plan, write the plan down, implement.
- Run only cheap self-checks, then **stop and show the result**; the user decides: change, continue, or review.
- **Never spawn a reviewer on your own initiative.**
- Gate `PASS` only when the user accepts it or a requested review has no open FATAL/SERIOUS findings. Else `USER_REVIEW` (`BLOCKED` = missing evidence or failed check).
- A change to an upstream input (netlist, parts, footprints, placement, routing, BOM, CPL) invalidates dependent gates; rerun, don't keep a stale `PASS`.

## Designer and reviewer agents

Main Claude coordinates and talks to the user. It may spawn a **designer** without asking; a **reviewer** only on request.

- **Designer:** does the work with the task's skills; the only agent that edits files. Brief: task, skills, input file paths. Stops and returns user-only questions immediately.
- **Reviewer (on request):** read-only; loads `/pcb:adversarial-review`, exports its own copies. Brief: file paths only, never the designer's conclusions.
- Never answer agent questions for the user.
- One feedback cycle: designer fixes FATAL/SERIOUS once, reviewer re-checks from a fresh export. Still open: stop and report finding, what was tried, options.
- Agents run sequentially, never editing concurrently.
- Pass file paths, not pasted content; copy measured numbers from original output.
- Designer on a cheaper model, reviewer on a stronger one; if unavailable, use the next one up and tell the user.

## Evidence tags

Tag every number and claim a decision rests on:

| Tag | Meaning |
|---|---|
| `VERIFIED` | From an authoritative source (datasheet, standard, live page, measurement); cite source and date |
| `COMPUTED` | Arithmetic on verified numbers, shown |
| `TARGET` | Design allocation with stated margin |
| `ESTIMATE` | Unmeasured/assumed; confirm before dependent gate |
| `NOT ESTABLISHED` | Unknown; needs owner and closing evidence |

- "Probably doesn't support Y" is not a finding; prove claims that decide whether work continues.
- Use current sources, not memory, for stock, price, limits.

## Decisions

- Record rulings in `DECISIONS.md` as `D-<n>` with evidence.
- Append-only: amendments supersede, old entries stay visible.

## Board versioning

- Versions are numbered **`v<major>.<minor>`**, starting at **v1.0**. `<rev>` everywhere in these skills means this string (e.g. `production/v1.1/`).
- **Minor step (v1.0 → v1.1):** fixes and tweaks that keep the board's outline, mounting, connector positions and pinouts, and architecture: routing/pour fixes, part value or equivalent-part swaps, silkscreen, test points, DRC/DFM fixes.
- **Major step (v1.x → v2.0):** major changes: new outline or mounting, moved/changed connectors or pinouts, new main IC or architecture, added/removed functional blocks, layer-count change. Minor resets to 0.
- Unsure whether a change is major: propose the number with the reason and let the user decide.
- A released version is never reused or patched: any change after `production/<rev>/` is released gets the next version.
- Show the version in the KiCad title block (schematic and board) and as top silkscreen text (`board-defaults.md` text size), and in `layout-review.json` `board_revision`.

## Working rules

- Edit the native source (or its generator), never only an export.
- Judge the saved file: save, close, reopen, re-export before calling a gate.
- Hand over between sessions through files.

# Part 2: PCB project session

## Start

1. Toolchain: the SessionStart hook already checked it. If it printed `[pcb] ...`, tell the user and stop on that item. Else read tool paths from `.pcba-workflow/env.json` (`kicad_cli`, `kicad_mcp_configured`) as `K`. No `env.json`: manual Preflight in [references/toolchain.md](references/toolchain.md).
2. If `pcb/template.*` is unrenamed, rename to the project name (ask only for the name; proceed even if KiCad is open, then give the close-without-saving reminder).
3. Establish the session (ask if unclear); use **only** its skills; open references only when needed.

`SK` = `${CLAUDE_SKILL_DIR}/..` (scripts in `$SK/<skill>/scripts/`).

## Session map

| Session | Skills | Produces |
|---|---|---|
| **1. Schematic** | `design-and-review-circuit`; `schematic-humanizer` (readability); `plan-board-bringup` (straps, programming, test points, DNP); `plan-electronic-product` only if no brief | schematic, `circuit-review.md` (with layout handoff constraints), `netlist-assertions.json`, draft `bringup-plan.md` |
| **2. Sourcing and footprints** | `qualify-pcba-sourcing` | `sourcing-lock.csv`, `MPN`/`LCSC` fields, checked footprints |
| **3. Layout** | `pcb-layout-review`; `plan-board-bringup` (test pads/runbook); `release-pcba-fabrication` at end | board, `layout-review.json`, release in `production/<rev>/` |

- `adversarial-review`: only on user request. `manage-pcba-program`: only for status, gate tracking, or re-opening a release.
- Sessions hand over through `.pcba-workflow/`.

## Checkpoints per session

- **Schematic:** plan in `circuit-review.md`/`DECISIONS.md`, implement, run only ERC + netlist assertions, stop.
- **Sourcing:** stop after sourcing lock and footprint assignment; double-check (MPN, LCSC, Basic/Extended, ratings, stock, land pattern, pin 1) only on request.
- **Layout:** user sets board size first; place sheet by sheet, stop after each placement; no pours or routing until placement approved; then pours + routing, stop again.

Models: designer `sonnet` (sourcing: `haiku`); reviewer `opus` (sourcing: `sonnet`).
