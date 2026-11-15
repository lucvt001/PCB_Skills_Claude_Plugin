---
name: design-and-review-circuit
description: Design or audit a circuit: architecture, power/reset/boot, ratings, timing, protection, netlist intent assertions, layout-facing constraints.
---

# Circuit Design Reviewer

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Readability and electrical correctness are separate gates. Default to review-only unless the user asks to change the circuit source.

## Establish truth

1. Read repo instructions, brief, architecture, `DECISIONS.md`, sourcing lock, native schematic/generator, netlist, BOM, datasheets, firmware-visible behavior, existing reviews.
2. Identify the electrical source of truth; if a generator owns the schematic, edit the generator.
3. Before any authorized correction capture ERC/lint, connectivity, and protected layout hashes.
4. **Read the datasheet of every IC, module, regulator, connector before designing/reviewing its circuit** (`pcb/datasheets/`). If an EVM/EVK PDF exists, treat its schematic, BOM, layout notes as the reference design and record every deviation in `DECISIONS.md`. Save tokens: table of contents first, then pin table, abs-max and recommended conditions, electrical characteristics at your operating point, typical application, component selection, layout guidelines. Missing datasheet: ask the user (or for permission to download); never design from memory.
5. Work from native KiCad source (`.kicad_sch`, libraries, netlist export; commands in `../pcb-layout-review/references/kicad-adapter.md`). PDF/image only: findings are transcription-limited; no electrical corrections without native source or trusted netlist.

## Schematic structure

- New schematic/sheet: [new-schematic-kicad.md](references/new-schematic-kicad.md). Always: [schematic-rules.md](references/schematic-rules.md) (datasheets first, ask about selectable IC options, designators, value formats, sheet layout).
- Block in the board (STM32, USB-C, CAN, RS-485, Ethernet, battery input, regulators, motor drive, I2C/LED/MOSFET): read only that section of [common-circuits.md](references/common-circuits.md); datasheet/EVM take precedence.
- **Large designs** (>1 page or ~40+ parts): hierarchical sheets, one per functional block, hierarchical labels and sheet pins on the parent. No global labels between sheets (power symbols are fine). Small single-page designs may use wires and local labels.
- **Designators, multi-sheet only** (single-sheet: R1, C1, U1): page x 100 + increment (R101, C201, U201). KiCad Annotate with "first free number after sheet number x 100", sorted by sheet. >99 of a prefix: split the page.
- Every symbol carries `MPN` and `LCSC` once sourcing has run.
- JLCPCB assembly defaults: [../workflow/references/jlcpcb-assembly.md](../workflow/references/jlcpcb-assembly.md).
- ERC passing is necessary, not sufficient: inspect the schematic PDF pages.
- Save used datasheets to `pcb/datasheets/`.

## Audit

Read [circuit-audit-checklist.md](references/circuit-audit-checklist.md); write `.pcba-workflow/circuit-review.md` from [assets/circuit-review.md](assets/circuit-review.md).

- Explain operating principle and data/power/control flow plainly.
- Build: component function table, power tree, voltage-domain table, operating-state table, reset/boot/ownership sequence.
- Trace every external interface, power entry, driver, receiver, memory/control path, hardware default; check partial-power and firmware-not-running states.
- Verify ratings, logic thresholds, enable polarity, unused pins, static ties, decoupling, regulator stability/thermal margin, protection, clocks/timing, connector semantics. Run the mandatory-pin sweep and "pass review, fail on the bench" patterns.
- **Assert intent against the netlist:** write `.pcba-workflow/netlist-assertions.json` from design intent (not the current netlist); run `${CLAUDE_SKILL_DIR}/scripts/assert_netlist.py` on a fresh KiCad XML export per [netlist-assertions.md](references/netlist-assertions.md). Include must-not-connect assertions for every rail pair and switch node.
- Classify findings critical/major/minor/information; distinguish proven defect, design risk, unknown evidence.
- Tag every number VERIFIED/COMPUTED/TARGET/ESTIMATE/NOT ESTABLISHED (see workflow skill). Layout constraints carry tags too: data/edge rate, topology/stubs, return plane, skew, current, placement, keepout, source.
- Boot straps, programming/recovery, test pads, DNP hedges go in the schematic before layout: coordinate with `/plan-board-bringup`.

## Correct only when authorized

Per change: state defect and evidence, edit the source of truth, render the full schematic and inspect it, rerun ERC/lint and netlist assertions, compare canonical connectivity, confirm protected layout files unchanged. A deliberate electrical change must appear in the connectivity delta and `DECISIONS.md`, never hidden in presentation cleanup.

## Gate

- `PASS`: no critical/major issue or safety-relevant unknown, netlist assertions pass, parts match the sourcing lock, and the user accepted (or a requested `/adversarial-review` has no open FATAL/SERIOUS).
- `USER_REVIEW`: explicit engineering decisions. `BLOCKED`: missing evidence or failed check.
- Hand off: readability `/schematic-humanizer`, part risk `/qualify-pcba-sourcing`, bring-up `/plan-board-bringup`, placement/routing constraints `/pcb-layout-review`.
