---
name: manage-pcba-program
description: Overall status, gate tracking, change invalidation, or re-opening a released design. Only on request.
---

# PCBA Program Manager

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Coordinate specialists; don't replace them. Shared artifacts default to `.pcba-workflow/`; gate status is only `PASS`, `BLOCKED`, or `USER_REVIEW`.

## Start

1. Read repo instructions; inventory descriptions, native EDA sources, generators, netlists, plots, PCB files, BOM/CPL, manufacturing packages, test evidence, `DECISIONS.md`, approvals.
2. Read [stage-gates.md](references/stage-gates.md).
3. Check which specialist skills are installed. Missing one: report its exact name and stop that stage; never improvise its approval.
4. Init/validate `.pcba-workflow/program-state.json` with `${CLAUDE_SKILL_DIR}/scripts/program_state.py`.

## Route

- Description or incomplete requirements: `/plan-electronic-product`
- BOM, MPN, stock, package, CAD, lifecycle, cost, substitution: `/qualify-pcba-sourcing`
- Architecture, ratings, power, reset, timing, safe state, netlist intent: `/design-and-review-circuit`
- Programming, recovery, test pads, staged power-up, DNP hedges, runbook: `/plan-board-bringup` (before placement freeze; finished before release)
- Label-heavy or floating schematic: `/schematic-humanizer` after a connectivity baseline; its result is never circuit approval
- Placement, routing, layers, planes, DRC, SI/PI, RF, mechanics, DFM: `/pcb-layout-review`
- Gerber, drill, BOM, CPL, 2D plots, release: `/release-pcba-fabrication`
- JLCPCB upload, part matching, placement preview, payment: done by the user, not tracked as stages; note outcomes in `DECISIONS.md` if a fix was needed.
- Before any `PASS`: user acceptance, or (on request) `/adversarial-review`. Never start a review automatically.
- Require sourcing and circuit gates before placement freeze.

## Evidence and change

- Record in program state: artifact paths, revisions, SHA-256, gate status, risks, review reports, approval evidence.
- `DECISIONS.md` rules: see workflow skill.
- Standing authority, when granted: operate only by recorded hard constraints and soft ranking; escalate constraint changes. Never covers substitution, placement, price approval, credentials, order submission, or payment.
- Invalidate downstream gates after controlled data changes with `${CLAUDE_SKILL_DIR}/scripts/program_state.py invalidate --change ...`; never manually keep a stale PASS.
- Only the substitution approval is tracked; payment is always the user's.
- Review-only requests don't authorize design edits, browser mutations, cart changes, or payments.
- Parallel workers must not edit the same files. KiCad open in the GUI doesn't block disk edits; finish with the workflow skill's close-without-saving reminder.
- Stop on contradictory revisions, missing source-of-truth data, unverifiable safety assumptions, or a specialist BLOCKED.

## Re-opening a released design

Move the withdrawn package to `production/superseded/<rev>/` with the exact reason (a superseded package beside the current one gets ordered eventually). Re-run each affected gate from a fresh export, not just the delta. Fix everything that's free while the board is open.

## Finish

Report current gate, completed evidence, invalidated work, risks, required user reviews, next specialist. Complete only when the requested terminal gate is PASS and no required work remains. Claude's work ends at a validated release; the user uploads, reviews the JLCPCB placement preview, orders, pays.
