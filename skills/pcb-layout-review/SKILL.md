---
name: pcb-layout-review
description: PCB placement, routability, stackup, routing, planes, DRC/DFM, and 2D placement mechanics; also porting a proven board to a variant.
---

# PCB Layout

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Rules live in three layers. Read them in this order, and **only what is relevant**:

| layer | file(s) | when to read |
|---|---|---|
| General | [references/general-rules.md](references/general-rules.md) | **in full, at the start of every session** |
| Defaults | [references/board-defaults.md](references/board-defaults.md) | in full, at the start of every session |
| Category | `references/rules/*.md` (index below) | per block, just before placing it and again before routing it |

## 1. Start of every layout session: mandatory

Before the first placement, routing, pour, or review action, and again after the session is resumed or the context is compacted:

1. **Read `general-rules.md` completely, even if you believe you remember it.** Skimming or relying on memory is how rules get dropped. It is kept short so that a full read is cheap.
2. **Read `board-defaults.md` completely.**
3. **Do not read the category files yet.** They're loaded per block (section 2). Reading every file up front buries the rules that matter by the time you need them.
4. Tell the user in one line that both files were read, then continue.

## 2. Load category rules per block (just in time)

Each category file has **Read when**, **Placement**, **Routing**, **Verify** sections and names related categories under **Also read**.

**Before placing a sheet:**

1. List the functional blocks and notable parts on it (e.g. buck regulator, USB-C, crystal, shunt, CAN transceiver).
2. Match each block to the index below by part type, net names, or sheet name. `power-routing-and-pours.md` applies to every board.
3. Read the **Placement** section of every matched file (and its **Also read** files when they apply), right before placing that block. Read it at least once in this session even if you've read it in an earlier one.
4. With the placement stop, post **"Rules applied"**: each file used and the 1-3 constraints that shaped the placement, so the user can see what governed it.

**Before routing a sheet (after the user approves placement):**

- Re-read the **Routing** and **Verify** sections of the same files. Placement and routing are separated by a user check; don't route from memory.
- Post "Rules applied" again with the routing stop.

**Trigger phrases:** when the user says **"apply stitching vias"**, re-read `board-defaults.md` section 5 "Stitching / pour-edge vias" before placing any via, and follow it exactly. When the user asks for a **copper pour**, re-read `board-defaults.md` section 6.

**Skip what isn't there:** don't open files for blocks that aren't on the board. If a block matches no category, follow its datasheet/EVM layout and the general rules, and tell the user it isn't covered (a candidate new category).

## 3. Category index (`references/rules/`)

| file | read when the sheet has... |
|---|---|
| [power-routing-and-pours.md](references/rules/power-routing-and-pours.md) | **every board**: rails, power traces/vias, GND pours, planes, stitching |
| [battery-input-and-protection.md](references/rules/battery-input-and-protection.md) | battery/DC input, fuse, reverse-polarity, input TVS, high-current bus |
| [switching-regulators.md](references/rules/switching-regulators.md) | buck, boost, buck-boost, inverting converter, inductor, SW node |
| [linear-regulators.md](references/rules/linear-regulators.md) | LDO, linear regulator |
| [thermal-power-parts.md](references/rules/thermal-power-parts.md) | exposed thermal pads, MOSFETs, hot parts |
| [current-sense-shunt.md](references/rules/current-sense-shunt.md) | shunt resistor + sense amplifier/ADC |
| [motor-drive.md](references/rules/motor-drive.md) | half/H/3-phase bridges, gate drivers, motor phases |
| [high-voltage-clearance.md](references/rules/high-voltage-clearance.md) | any net pair >= 31 V peak, wet environment |
| [crystals-and-clocks.md](references/rules/crystals-and-clocks.md) | crystals, resonators, oscillators, clock nets |
| [fine-pitch-ics-and-fanout.md](references/rules/fine-pitch-ics-and-fanout.md) | QFN/QFP/BGA/LGA <= 0.65 mm pitch, dense MCU/FPGA/PHY |
| [differential-pairs-and-impedance.md](references/rules/differential-pairs-and-impedance.md) | any differential pair or impedance-controlled net |
| [usb.md](references/rules/usb.md) | USB connector, D+/D-, VBUS |
| [ethernet.md](references/rules/ethernet.md) | PHY, magnetics, RJ45 |
| [can-rs485.md](references/rules/can-rs485.md) | CAN, RS-485/422 transceiver, bus termination |
| [digital-buses.md](references/rules/digital-buses.md) | I2C, SPI, UART, QSPI/SDIO, parallel/memory buses |
| [analog-and-adc.md](references/rules/analog-and-adc.md) | op-amps, ADC inputs, references, sensor front-ends |
| [modules-rf-and-antennas.md](references/rules/modules-rf-and-antennas.md) | radio modules, castellated/LGA modules, antennas, RF feeds |
| [connectors.md](references/rules/connectors.md) | any connector; switches/LEDs/buttons at the board edge |
| [dense-connectors-and-board-stacks.md](references/rules/dense-connectors-and-board-stacks.md) | card-edge, board-to-board, sockets, daughtercards, dense fanout |
| [test-points-and-fiducials.md](references/rules/test-points-and-fiducials.md) | bring-up test/strap pads, fiducials |
| [mechanical-fit-and-assembly.md](references/rules/mechanical-fit-and-assembly.md) | enclosure, mounting holes, through-hole, hand-fit parts |
| [autorouting-and-experiments.md](references/rules/autorouting-and-experiments.md) | running an autorouter, comparing layout candidates |
| [variant-porting.md](references/rules/variant-porting.md) | derivative of a proven board |

When a new kind of block keeps coming up, add a category file with the same four sections and a row here; keep rules that apply to every board in `general-rules.md` only, never duplicated in a category.

## 4. Workflow

1. **Session start** (section 1), then establish truth (`general-rules.md` section 3).
2. **Per sheet, placement:** load categories (section 2) → place → routability check (`general-rules.md` section 5) → plots → "Rules applied" → **stop for the user**.
3. **Per sheet, pours and routing:** re-read Routing/Verify → route → verify (`general-rules.md` sections 6-7) → "Rules applied" → **stop for the user**.
4. **Whole board:** manufacturing and visual pass, release gate (`general-rules.md` sections 8-9).

## Tools and records

- KiCad CLI and MCP commands: [references/kicad-adapter.md](references/kicad-adapter.md).
- Gate record: [references/layout-review-record.md](references/layout-review-record.md) → `.pcba-workflow/layout-review.json`.
- `scripts/score_experiment.py` (experiments) and `scripts/record_lesson.py` (project lessons) write to `.pcba-workflow/`, never the installed skill.
